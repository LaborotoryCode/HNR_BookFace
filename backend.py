from supabase import create_client, Client
from face_rec import identify_user
import time
import os

url = ""
key = ""
supabase: Client = create_client(url, key)

response = supabase.storage.list_buckets()
print("response", response)

while 4<5:
    latest_new = supabase.storage.from_("new_user").list(
        "",
        {"limit": 1, "sortBy": {"column": "name", "order": "desc"}},
    )
    latest_retrieve = supabase.storage.from_("Retrieve").list(
        "",
        {"limit": 1, "sortBy": {"column": "name", "order": "desc"}},
    )

    if len(latest_new)>=1:
        name_uuid = latest_new[0]["name"]

        with open(f"faces/{name_uuid}", "wb+") as f:
            response = supabase.storage.from_("new_user").download(
                name_uuid
            )
            f.write(response)

        empty = supabase.storage.empty_bucket("new_user")
        print("User Registered")

    elif len(latest_retrieve)>=1:
        print("analysing")

        with open("retrieve/retrieve.jpg", "wb+") as f:
            response = supabase.storage.from_("Retrieve").download(
                "retrieve.jpg"
            )
            f.write(response)
        
        face_rec = identify_user("retrieve/retrieve.jpg")

        if face_rec != 1:
            upload = (
                supabase.table("Retrieve")
                .insert({"id": face_rec})
                .execute()
            )

            empty = supabase.storage.empty_bucket("Retrieve")
        else:
            upload = (
                supabase.table("Retrieve")
                .insert({"id": "nil"})
                .execute()
            )

            empty = supabase.storage.empty_bucket("Retrieve")
            os.remove("retrieve/retrieve.jpg")

        print("recognised")