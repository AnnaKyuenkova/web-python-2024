def is_valid_email(email):
    parts = email.split('@')
    if len(parts) != 2:
        return False
    username = parts[0]
    website_extension = parts[1].split('.')
    if len(website_extension) != 2:
        return False
    website = website_extension[0]
    extension = website_extension[1]
    if not username.replace('-', '').replace('_', '').isalnum():
        return False
    if not website.isalnum():
        return False
    if not extension.isalpha() or len(extension) > 3:
        return False
    return True

def fun(N, emails):
    valid_emails = [email for email in emails if is_valid_email(email)]
    return sorted(valid_emails)

if __name__ == '__main__':
    N = int(input())
    emails = [input() for _ in range(N)]
    
    result = fun(N, emails)
    print(result)