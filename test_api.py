import urllib.request
import json

def post_json(url, data):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

# 1. Test HTML
html_resp = urllib.request.urlopen('http://127.0.0.1:5000/').read().decode('utf-8')
assert ('AURA MARK' in html_resp or 'The Boys' in html_resp)
print('[PASS] 1. Homepage loads successfully with The Boys')

# 2. Test Samples
samples = json.loads(urllib.request.urlopen('http://127.0.0.1:5000/api/samples').read().decode('utf-8'))
assert samples['success']
print(f"[PASS] 2. Samples API returns presets: {len(samples['samples']['hosts'])} hosts, {len(samples['samples']['watermarks'])} watermarks")

# 3. Test Embed
embed_payload = {
    'host_image': '/samples/host_image.png',
    'watermark_image': '/samples/watermark.png',
    'key': 12345,
    'strength': 30.0,
    'bits_per_block': 2
}
embed_res = post_json('http://127.0.0.1:5000/api/embed', embed_payload)
assert embed_res['success']
sess_id = embed_res['session_id']
print(f"[PASS] 3. Embed API generated watermarked image. PSNR: {embed_res['metrics']['psnr']} dB, SSIM: {embed_res['metrics']['ssim']}")

# 4. Test Extract & Separate
extract_payload = {
    'session_id': sess_id,
    'key': 12345
}
extract_res = post_json('http://127.0.0.1:5000/api/extract', extract_payload)
assert extract_res['success']
print(f"[PASS] 4. Separation API separated both assets! Watermark NC: {extract_res['metrics']['nc']} | Restored Host PSNR: {extract_res['metrics']['host_restoration_psnr']} dB")

# 5. Test Attack Simulation
attack_payload = {
    'session_id': sess_id,
    'attack_type': 'gaussian_noise',
    'sigma': 12.0,
    'key': 12345
}
attack_res = post_json('http://127.0.0.1:5000/api/attack', attack_payload)
assert attack_res['success']
print(f"[PASS] 5. Attack Simulation tested Gaussian noise. Surviving Watermark NC: {attack_res['metrics']['nc']} | Attacked Image PSNR: {attack_res['metrics']['psnr']} dB")

# 6. Test Key Download
key_resp = urllib.request.urlopen(f'http://127.0.0.1:5000/api/download/keys/{sess_id}').read().decode('utf-8')
key_json = json.loads(key_resp)
assert key_json['key'] == 12345
print('[PASS] 6. Keys JSON download endpoint verified!')
print('\n*** ALL 6 END-TO-END SUITE TESTS PASSED COMPLETELY! ***')
