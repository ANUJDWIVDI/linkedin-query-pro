from flask import Flask, render_template, request, send_file
from linkedin_api import Linkedin
from openpyxl.workbook import Workbook

app = Flask(__name__)

@app.route('/')
def index():
    popular_keywords = ['programming', 'coding', 'web', 'mobile', 'cloud', 'artificial', 'intelligence', 'machine',
                        'learning', 'data', 'analytics', 'cyber', 'security', 'blockchain', 'devops', 'automation',
                        'iot', 'robotics', 'virtualization', 'augmented']
    popular_locations = ['Bangalore', 'Mumbai', 'Hyderabad', 'Chennai', 'Pune', 'Gurgaon', 'Noida', 'Delhi',
                         'Ahmedabad', 'Kolkata', 'Jaipur', 'Chandigarh', 'Surat', 'Lucknow', 'Kanpur', 'Nagpur',
                         'Patna', 'Bhopal', 'Ludhiana', 'Agra']

    return render_template('home.html', popular_keywords=popular_keywords, popular_locations=popular_locations)


@app.route('/submit', methods=['POST'])
def api_fetch():
    email = request.form['email']
    password = request.form['password']
    search_keywords = request.form.getlist('search_keywords')
    locations = request.form.getlist('locations')


    print(f"email: {email}")
    print(f"password: {password}")
    print(f"search_keywords: {search_keywords}")
    print(f"locations: {locations}")

    # Authenticate with LinkedIn using your credentials
    api = Linkedin(email, password)

    # Define search query
    query = f"keywords:{','.join(search_keywords)} location:{','.join(locations)}"

    print(" ---  STARTING SEARCH  ---")

    search_results = api.search_people(keywords=query, limit=500)

    print(" ---  END SEARCH  ---")

    # Save data in a spreadsheet
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Search Results'
    worksheet.append(['Search Query', query])
    worksheet.append(list(search_results[0].keys()))
    # Add data fetched from API to worksheet
    for person in search_results:
        row = [person.get(field, '') for field in search_results[0].keys()]
        worksheet.append(row)

    worksheet.append(['Name', 'Email', 'Phone'])


    for person in search_results:
        name = person.get('name', '')
        email = person.get('email_address', '')
        phone = person.get('phone_numbers', [''])[0]
        worksheet.append([name, email, phone])

    # Save the workbook
    workbook.save('search_results.xlsx')

    return render_template('result.html', data=search_results)



@app.route('/download')
def download_file():
    path = "search_results.xlsx"
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
