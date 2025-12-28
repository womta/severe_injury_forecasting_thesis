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


# Missing Data Heatmap
def missing_data_heatmap(cloud, df, features, date_col = 'date_time', ticker_col = 'ticker'):
  
    # Ensure date_time is datetime and sorted
    df = df.to_pandas()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)

    # Count missing values per row for the given features
    df['missing_count'] = df[features].isna().sum(axis=1)

    # Aggregate per time/ticker
    pivot_df = df.pivot_table(
        index=date_col,
        columns=ticker_col,
        values='missing_count',
        aggfunc='sum',
        fill_value=0
    )

    # Plot heatmap with tickers on the x-axis
    fig = px.imshow(
        pivot_df,  
        labels=dict(x="Ticker", y="Date/Time", color="Missing Features"),
        x=pivot_df.columns,
        y=pivot_df.index,
        aspect="auto",
        color_continuous_scale = [global_vars.MEDIUM_COLOR, global_vars.LOW_COLOR]  # present = light gray, missing = red
    )

    fig.update_layout(
        title="Missing Data Heatmap",
        xaxis_title="Ticker",
        yaxis_title="Date/Time",
        yaxis_autorange="reversed"  # ✅ time flows top-to-bottom
    )

     # Store Viz Object
    if(cloud):
        store_plotly_object(fig, global_vars.VIZ_MISSING_PATH)
    else:
        store_plotly_object(fig, global_vars.VIZ_MISSING_PATH)
        fig.show()




# Check the size of the Test and Train Data
def check_test_train_data(train_df, test_df):
		
		nrow_train_df = len(train_df)
		nrow_test_df = len(test_df)

		unique_dates_train = sorted(train_df['date'].dt.date.unique(), reverse = True)
		unique_dates_test = sorted(test_df['date'].dt.date.unique(), reverse = True)

		print(f''''
		####	Records		####
		Train Data Contains: {nrow_train_df} Records
		Test Data Contains: {nrow_test_df} Records
		Complete Data Contains: {nrow_train_df + nrow_test_df} Records
		
		####	 Days		####
		Unique days in Train Set: {len(unique_dates_train)}
		Unique days in Test Set: {len(unique_dates_test)}
		Total Unique days: {len(unique_dates_test) + len(unique_dates_train)}
		''')


# Calculate and add UMAP
def create_umap(df, features):
	#python -m pip install numba==0.61.0rc2
	#pip install umap-learn
	import umap

	# Apply UMAP on the factor scores
	umap_model = umap.UMAP(n_components = 3, n_neighbors = 80, min_dist = 0.3, random_state = settings.RANDOM_STATE)
	UMAP = umap_model.fit_transform(df[features])
	UMAP = pd.DataFrame(UMAP, columns=['UMAP_01', 'UMAP_02', 'UMAP_03'])

	# Reset indices of both DataFrames
	UMAP.reset_index(drop = True, inplace = True)
	df.reset_index(drop = True, inplace = True)

	df = pd.concat([df, UMAP], axis = 1)
	return df


