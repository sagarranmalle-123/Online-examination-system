import subprocess, os

with open('test_page.html', 'w', encoding='utf-8') as f:
    f.write('<html><body style="background:lightblue;color:darkblue;font-size:30px;padding:50px;">Hello Test Edge</body></html>')

abs_html = os.path.abspath('test_page.html')
edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
cmd = [edge_path, '--headless', '--disable-gpu', f'--screenshot={os.path.abspath("test_page.png")}', '--window-size=800,600', f'file:///{abs_html}']
print('Running Edge...')
res = subprocess.run(cmd, capture_output=True, text=True)
print('Return code:', res.returncode)
print('File exists:', os.path.exists('test_page.png'))
if os.path.exists('test_page.png'):
    print('Size:', os.path.getsize('test_page.png'))

