echo "select * from dim_vehicle" | sudo mysql -u root -p circledb | sed 's/\t/,/g' > mvt_dim_vehicle.csv
