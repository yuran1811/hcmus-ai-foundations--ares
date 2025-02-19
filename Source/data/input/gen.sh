for i in $(seq 1 1 35); do
    if [ $i -lt 10 ];
	then
        filename="input-0$i.txt"
    else
        filename="input-$i.txt"
    fi

	touch "$filename"
done