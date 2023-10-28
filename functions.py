import requests

url = 'https://www.gosuslugi.ru/api/lk/v1/feeds/'
headers = {
    'Cookie': 'feed_mig=S; userSelectedLanguage=ru; nau=e912456c-b3c0-104f-f829-e88d559f9e56; _ym_uid=1696067047943934652; _ym_d=1696067047; cfidsgib-w-gosuslugi=; _idp_authn_id=phone%3A%252B7(923)3770575; usi_portal=rBApZGU8+4t0xlaSojVAAg==; ns-nlb=ffffffffaf18369e45525d5f4f58455e445a4a423660; fhp=rBBoEGU8+4wnKH8vhM82Ag==; NSC_q00qhvtubu=ffffffffaf18375245525d5f4f58455e445a4a423660; _ym_isad=2; strelets=bde918d23dc993e4d30531bd5a091940; __gsac_gib-w-gosuslugi=4c60862e-b38b-4a24-dd06-382ebe14492b; __zzatgib-w-gosuslugi=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2VrTXdcdF5+Jz5ZHD9AMRlFK0BXCRwaSk5fbxt7Il8qCCRjNV8ZQ2pODWk3XBQ8dWU+R3Z7LURqIGZLXCREUT9IXl1JEjJiEkBATUcNN0BeN1dhMA8WEU1HFT1WUk9DKGsbcVhXL3AkF0hSfjsWa25HZ0dXTBdfQjs4WEERdV1BQ291Lz1pHlFDS194Hxg6aF17CTdlHDx/TQl6MjAbRWYjaE9bJENWTwouHRVzXWoQS0NufAgwNF4tb2EpFBYbNSEeQVoLG2kzXwhASSdyETlldhA=PP0bEA==; u=242226241; userSelectedRegion=04401000000; org-roles-count={"L":1,"B":0}; prev-gu-role=P; acc_t=eyJ2ZXIiOjEsInR5cCI6IkpXVCIsInNidCI6ImFjY2VzcyIsImFsZyI6IlJTMjU2In0.eyJuYmYiOjE2OTg0OTU0MTksInNjb3BlIjoiaHR0cDpcL1wvZXNpYS5nb3N1c2x1Z2kucnVcL3Vzcl9pbmY_bW9kZT13Jm9pZD0yNDIyMjYyNDEgaHR0cDpcL1wvZXNpYS5nb3N1c2x1Z2kucnVcL3Vzcl9zZWM_bW9kZT13Jm9pZD0yNDIyMjYyNDEgaHR0cDpcL1wvZXNpYS5nb3N1c2x1Z2kucnVcL3Vzcl90cm0_bW9kZT13Jm9pZD0yNDIyMjYyNDEiLCJpc3MiOiJodHRwOlwvXC9lc2lhLmdvc3VzbHVnaS5ydVwvIiwidXJuOmVzaWE6c2lkIjoiYTcyY2FmNGItMjUxMS00NjZhLTk3ZDAtM2NmZjk4MTdhZmIzIiwidXJuOmVzaWE6c2JqX2lkIjoyNDIyMjYyNDEsImV4cCI6MTY5ODUzMTQxOSwiaWF0IjoxNjk4NDk1NDE5LCJjbGllbnRfaWQiOiJQR1UifQ.OgajETZaLmlo0EftWtQEL3kjRQv2bvrCGea-KEbqwdzxYjBBbcTy6K5DWleiE3SvNNagAzBbOuuhoCaqtQ81fCr5HH_AWKogvm_VBRNcGKCpNL1f2-7dpSZdXLZQ42c_u4NMq-4P_kp6Wq65ol2koJUT99rgCa-cdQsXO0wR_j4hE9h5mnEr3fqsLQ8jnJ2wGrZceYGZT26HSKzanuCKl4Tzgo2hEoQpMiw9PDoPpnv-r7HyYJ9vQ1PexxXjnIf3dG_DT8oNFsoXB1e80QIHDWipr642E6yh0BW6k_vDb904taB63_8So56Lt6Do6WIdp9mv6nfi_zZ9eqV6ExwifA; TS014d06c8=01474e7625906c862ca18bb618093c7dde593b11e0392ed47ab2c017a1c26fba6c27743a5b00aab6902070517195301f7734a2c88b2f11a15f4aad3b7483b820487d5c4c8bb66febd020718746935187585700af25858feda4a52387396ad74fa99ccd3c89ad1f81f86ab7fae32b91aad7ec2d8257; gu-content-role=P'
}
params ={
    'types': 'GEPS',
    'startDate': ''
}

r = requests.get(url=url, headers=headers, params=params)
items = r.json().get('items')
counter = 0
for i in items:
    if 'Постановление' in i.get('subTitle'):
        print(i)
        counter += 1
        print(counter)
