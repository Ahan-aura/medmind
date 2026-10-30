import urllib.request
import urllib.error
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. Health
with urllib.request.urlopen(urllib.request.Request('https://medmind-five.vercel.app/api/health'), context=ctx, timeout=10) as resp:
    print('Health status:', resp.status, resp.read().decode('utf-8'))

# 2. Login
login_data = json.dumps({'email': 'student@medmind.ai', 'password': 'student123'}).encode('utf-8')
req = urllib.request.Request('https://medmind-five.vercel.app/api/auth/login', data=login_data, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
    token = json.loads(resp.read().decode('utf-8'))['access_token']
    print('Login successful!')

# 3. List Lessons
req_lessons = urllib.request.Request('https://medmind-five.vercel.app/api/lessons', headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req_lessons, context=ctx, timeout=10) as resp:
    print('Lessons status:', resp.status)
    lessons = json.loads(resp.read().decode('utf-8'))
    print('Total lessons fetched on Vercel:', len(lessons))
    for l in lessons[:8]:
        print(f" - {l['id']}: {l['title']} (mins: {l['estimated_minutes']}, level: {l['difficulty']})")

# 4. Detail Lesson
req_detail = urllib.request.Request('https://medmind-five.vercel.app/api/lessons/LESSON-01', headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req_detail, context=ctx, timeout=10) as resp:
    detail = json.loads(resp.read().decode('utf-8'))
    print('\nLESSON-01 details:')
    print(' Title:', detail['title'])
    print(' Outcomes count:', len(detail['learning_outcomes']))
    print(' Key points count:', len(detail['key_points']))
    print(' Quick check questions count:', len(detail['quick_check']))
    print(' References loaded:', list(detail['references'].keys()))

# 5. Submit Quiz on Vercel
quiz_payload = json.dumps({'answers': {'Q1': 'A', 'Q2': 'B', 'Q3': 'C'}}).encode('utf-8')
req_quiz = urllib.request.Request(
    'https://medmind-five.vercel.app/api/lessons/LESSON-01/quiz',
    data=quiz_payload,
    headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
)
with urllib.request.urlopen(req_quiz, context=ctx, timeout=10) as resp:
    qres = json.loads(resp.read().decode('utf-8'))
    print('\nQuiz submission result on Vercel:')
    print(f" Score: {qres['score']}/{qres['max_score']} (Passed: {qres['passed']})")
    print(f" Best score: {qres['best_score']}")
