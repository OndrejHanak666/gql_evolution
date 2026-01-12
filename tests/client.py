import aiohttp
import uuid
def createGQLClient():

    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from src import DBDefinitions

    def ComposeCString():
        return "sqlite+aiosqlite:///:memory:"
    
    DBDefinitions.ComposeConnectionString = ComposeCString

    import main
    
    client = TestClient(main.app, raise_server_exceptions=False)
    return client


async def getToken(
    username, 
    password,
    keyurl = "http://localhost:33001/oauth/login3"
):
    
    async with aiohttp.ClientSession() as session:
        async with session.get(keyurl) as resp:
            print(resp.status)
            keyJson = await resp.json()
            print(keyJson)

        payload = {"key": keyJson["key"], "username": username, "password": password}
        async with session.post(keyurl, json=payload) as resp:
            print(resp.status)
            tokenJson = await resp.json()
            print(tokenJson)
    return tokenJson.get("token", None)
            

def createFederationClient(
    username="john.newbie@world.com", 
    password="john.newbie@world.com",
    gqlurl="http://localhost:8001/gql"
):
    token = None
    async def post(query, variables):
        nonlocal token
        if token is None:
            token = await getToken(username, password)

        payload = {"query": query, "variables": variables}
        # headers = {"Authorization": f"Bearer {token}"}
        cookies = {'authorization': token}
        async with aiohttp.ClientSession() as session:
            # print(headers, cookies)
            async with session.post(gqlurl, json=payload, cookies=cookies) as resp:
                # print(resp.status)
                if resp.status != 200:
                    text = await resp.text()
                    print(text)
                    return text
                else:
                    response = await resp.json()
                    return response
    return post

#def test_query_publications(responsejson):

async def main():
    client = createFederationClient()


    # ==========================================
    # 1. MUTACE: publicationInsert
    # ==========================================
    print("--- MUTATION: publicationInsert ---")
    
    # Vygenerujeme si unikátní ID, abychom mohli test pouštět opakovaně
    new_pub_id = str(uuid.uuid4())
    
    # Definice mutace s proměnnými ($id, $name, ...)
    # Všimni si, že přidávám i větev pro úspěch (např. ... on PublicationGQLModel), 
    # aby ses dozvěděl výsledek, nejen chybu.
    mutation_pub = """
    mutation($id: UUID!, $name: String!, $place: String!, $ref: String!) {
      publicationInsert(
        publication: {id: $id, name: $name, place: $place, reference: $ref}
      ) {
        __typename
        
        # Co se vrátí při úspěchu (uprav podle svého modelu, asi to bude PublicationGQLModel)
        ... on PublicationGQLModel {
            id
            lastchange
            name
        }

        # Co se vrátí při chybě (tvůj příklad)
        ... on PublicationGQLModelInsertError {
          code
          msg
          failed
        }
      }
    }
    """

    # Hodnoty proměnných
    variables_pub = {
        "id": new_pub_id,
        "name": "Automatický Test",
        "place": "Brno - Server",
        "ref": "www.test.cz"
    }

    result_pub = await client(mutation_pub, variables_pub)
    print(result_pub)
    
    # 1. Původní test: Publication Page
    print("--- TEST: publicationPage ---")
    query_pub = "{ publicationPage { id name place } }"
    result_pub = await client(query_pub, {})
    print(result_pub)

    # 2. Nový test: Publication Author Page
    # Předpokládám, že autoři mají jméno a příjmení
    print("\n--- TEST: publicationAuthorPage ---")
    query_author = """
    query {
        publicationAuthorsPage {
            id
            userId
            publicationId
            order
            share
        }
    }
    """
    result_author = await client(query_author, {})
    print(result_author)

    # 3. Nový test: Publication Type Page
    print("\n--- TEST: publicationTypePage ---")
    query_type = """
    query {
        publicationTypePage {
            id
            name
            nameEn
            categoryId
        }
    }
    """
    result_type = await client(query_type, {})
    print(result_type)

    # 4. Nový test: Publication Category Page
    print("\n--- TEST: publicationCategoryPage ---")
    query_category = """
    query {
        publicationCategoryPage {
            id
            name
            nameEn
        }
    }
    """
    result_category = await client(query_category, {})
    print(result_category)
    

if __name__ == "__main__":
    
    import asyncio
    asyncio.run(main())
    