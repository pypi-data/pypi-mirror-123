## Latest Earthquake in Indonesia 

### How it works
This package will retrieve latest earthquake information from [BMKG](https://bmkg.go.id)

### Author
Nasir Nooruddin

### Email
nasir@nasir.id

### How to use this package
install command :

    pip install requests
    pip install beautifulsoup4
    pip install bmkgnasir

Insert following scripts into your main.py

    from bmkg import extract, show
    if __name__ == '__main__':
        result = extract()
        show(result)