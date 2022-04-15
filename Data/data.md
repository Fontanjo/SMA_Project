This folder should contain:


- mubi_lists_data.parquet
- mubi_movie_data_0.parquet
- mubi_movie_data_1.parquet
    - splitted to upload to github
    - after loading, merge the two with pd.concat([df0, df1])
- mubi_ratings_data.parquet
- ~~mubi_db.sqlite~~
    - very big, probably not useful
- ~~mubi_lists_user_data.csv~~
    - useless (columns: ['user_id', 'list_id', 'list_update_date_utc', 'list_creation_date_utc', 'user_trialist', 'user_subscriber', 'user_avatar_image_url', 'user_cover_image_url', 'user_eligible_for_trial', 'user_has_payment_method'])
- ~~mubi_ratings_user_data.csv~~
    - useless (columns: 'user_id', 'rating_date_utc', 'user_trialist', 'user_subscriber', 'user_avatar_image_url', 'user_cover_image_url', 'user_eligible_for_trial', 'user_has_payment_method'])
