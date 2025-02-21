prompt_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume</title>
    <style>
        body {{ font-family: 'Times New Roman', Times, serif;  margin: 0; padding: 0; background-color: white; max-width: 800px; color:black }}
        h1 {{ font-size: 18px; text-align: center;  margin-bottom: 2px; }}
        .contact-info {{ text-align: center; font-size: 12px; margin-bottom: 2px; }}
        .contact-info a {{ color: #3498db; text-decoration: none; margin: 0; }}
        h2 {{ font-size: 14px; color: black; border-bottom: 2px solid black; padding-bottom: 1px ; margin: 0; }}
        h3 {{ font-size: 13px; color: black; padding-bottom: 1px ; margin: 0; }}
        .section {{ margin-bottom: 15px; }}
        .entry {{ background: #ffffff; padding: 1px; }}
        .entry-header {{ font-weight: bold; color: black }}
        .entry-details {{ font-size: 10px; color:black }}
        .education {{ font-size: 12px; color: black; padding:1px; margin: 0px; }}
        ul {{ padding: 0px; font-size: 12px; color:black }}
        ul li {{ margin-bottom: 1px; }}
        p {{ margin: 0; padding: 0; font-size: 12px; color:black }}
    </style>
</head>
<body>
    <h1>{name}</h1>
    <div class="contact-info">
        {email} | {phone} | {location} {linkedin} {github} {portfolio}
    </div>

    <h2>SUMMARY</h2>
    <p>{summary}</p>

    <h2>EDUCATION</h2>
    {education}

    <h2>TECHNICAL SKILLS</h2>
    <ul>
        {skills}
    </ul>

    <h2>PROFESSIONAL EXPERIENCE</h2>
    {experience}

    <h2>PROJECTS</h2>
    {projects}

    <h2>CERTIFICATIONS & ACHIEVEMENTS</h2>
    <ul>
        {certifications}
    </ul>
</body>
</html>
"""
