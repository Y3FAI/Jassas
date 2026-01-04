import cloudscraper
import sys

def test_access(url):
    print(f"[-] Initializing CloudScraper for: {url}")

    # Configuration matches src/crawler/fetcher.py exactly
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'darwin', # Keeps the user-agent signature consistent with Jassas
            'desktop': True
        }
    )

    try:
        print("[-] Attempting GET request...")
        response = scraper.get(url, timeout=30)
        
        print(f"[-] Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("\n[+] SUCCESS: Connection established.")
            print(f"[+] Content Length: {len(response.text)} bytes")
            print("[+] Title Preview: ", end="")
            
            # Simple check for title to verify it's actual HTML
            if "<title>" in response.text:
                start = response.text.find("<title>") + 7
                end = response.text.find("</title>")
                print(response.text[start:end].strip())
            else:
                print("(No title tag found)")
                
        elif response.status_code == 403:
            print("\n[!] FAILURE: 403 Forbidden.")
            print("    This likely means Cloudflare detected the bot/server IP.")
            
        else:
            print(f"\n[!] FAILURE: Unexpected status code {response.status_code}")

    except cloudscraper.exceptions.CloudflareChallengeError as e:
        print(f"\n[!] ERROR: Cloudflare Challenge Failed. \n    {e}")
    except Exception as e:
        print(f"\n[!] ERROR: Connection failed. \n    {type(e).__name__}: {e}")

if __name__ == "__main__":
    # Default to mygov.sa if no argument provided
    target = sys.argv[1] if len(sys.argv) > 1 else "https://my.gov.sa"
    test_access(target)