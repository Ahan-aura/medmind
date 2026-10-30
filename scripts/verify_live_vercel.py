import socket
import urllib.request
import urllib.error
import json
import ssl

# Bypass local router DNS timeout by pointing directly to Vercel Anycast edge IP
orig_getaddrinfo = socket.getaddrinfo
def custom_getaddrinfo(host, port, *args, **kwargs):
    if host == 'medmind-five.vercel.app':
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('76.76.21.21', port))]
    return orig_getaddrinfo(host, port, *args, **kwargs)
socket.getaddrinfo = custom_getaddrinfo

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print("=== 1. Health Endpoint ===")
try:
    with urllib.request.urlopen(urllib.request.Request('https://medmind-five.vercel.app/api/health', headers={'User-Agent': 'Mozilla/5.0'}), context=ctx, timeout=20) as resp:
        print('Health status:', resp.status)
        print(resp.read().decode('utf-8'))
except Exception as e:
    print('Health error:', e)

print("\n=== 2. Authentication ===")
login_data = json.dumps({'email': 'student@medmind.ai', 'password': 'student123'}).encode('utf-8')
req = urllib.request.Request('https://medmind-five.vercel.app/api/auth/login', data=login_data, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
    token = json.loads(resp.read().decode('utf-8'))['access_token']
    print('Login successful!')

auth_headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

print("\n=== 3. Patient Cases Listing ===")
req_cases = urllib.request.Request('https://medmind-five.vercel.app/api/cases', headers=auth_headers)
with urllib.request.urlopen(req_cases, context=ctx, timeout=20) as resp:
    cases = json.loads(resp.read().decode('utf-8'))
    print(f'Total cases on Vercel: {len(cases)}')
    for c in cases:
        print(f" - {c.get('id')}: {c.get('title')} ({c.get('learning_objective')})")

print("\n=== 4. Practice Lessons Listing ===")
req_lessons = urllib.request.Request('https://medmind-five.vercel.app/api/lessons', headers=auth_headers)
with urllib.request.urlopen(req_lessons, context=ctx, timeout=20) as resp:
    lessons = json.loads(resp.read().decode('utf-8'))
    print(f'Total lessons on Vercel: {len(lessons)}')
    for l in lessons:
        print(f" - {l.get('id')}: {l.get('title')}")

print("\n=== 5. AI Assistant Prompts ===")
req_prompts = urllib.request.Request('https://medmind-five.vercel.app/api/assistant/prompts', headers=auth_headers)
with urllib.request.urlopen(req_prompts, context=ctx, timeout=20) as resp:
    prompts_data = json.loads(resp.read().decode('utf-8'))
    print('Categories:', [g['category'] for g in prompts_data.get('groups', [])])

print("\n=== 6. AI Assistant Chat Query ===")
chat_payload = json.dumps({
    'message': 'How do I differentiate iron deficiency from beta-thalassaemia trait using FBC indices?'
}).encode('utf-8')
req_chat = urllib.request.Request('https://medmind-five.vercel.app/api/assistant/chat', data=chat_payload, headers=auth_headers)
with urllib.request.urlopen(req_chat, context=ctx, timeout=30) as resp:
    chat_res = json.loads(resp.read().decode('utf-8'))
    print('Model:', chat_res.get('model'))
    print('Citations:', [c['ref_id'] for c in chat_res.get('citations', [])])
    print('Recommended Lessons:', [l['id'] for l in chat_res.get('recommended_lessons', [])])
    print('Suggested Questions count:', len(chat_res.get('suggested_questions', [])))
    print('Reply excerpt:', chat_res.get('reply', '')[:180].replace('\n', ' '))

print("\n=== 7. Frontend Routes ===")
for path in ['/', '/cases', '/lessons', '/assistant']:
    req_spa = urllib.request.Request('https://medmind-five.vercel.app' + path, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_spa, context=ctx, timeout=20) as resp:
        print(f'Frontend {path} -> {resp.status}')
