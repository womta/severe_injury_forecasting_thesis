
#########################
# Visualization Objects #
#########################

# Create an HTML data table
def create_table(df):
    
    # Enhanced HTML table with styling
    html_table = df.to_html(
        index = False, 
        classes = 'table table-bordered table-striped', 
        border = 0, 
        justify = 'center', 
        table_id = 'my_table' 
    )

    # Add CSS for further customization
    css = """
    <style>
    #my_table {
        width: auto !important; /* Adjust table width as needed */
        margin: 20px auto; /* Center the table */
        border-collapse: collapse;
    }
    #my_table th, #my_table td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: center;
    }
    #my_table th {
        background-color: #f2f2f2;
    }
    </style>
    """

    # Combine HTML table and CSS
    html_string = f"{css}\n{html_table}"

    # Save to HTML file
    with open('DATA/test.html', 'w') as f:
        f.write(html_string)

    return True


