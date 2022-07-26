class CarBrands:

    def __init__(self):
        self.brands = {
            'abarth': 'abarth', 'alfa': 'alfa romeo', 'alpine': 'alpine', 'aston': 'aston martin',
            'audi': 'audi', 'bentley': 'bentley', 'bugatti': 'bugatti', 'chevrolet': 'chevrolet', 
            'chrysler': 'chrysler', 'citroen': 'citroen', 'cupra': 'cupra', 'dacia': 'dacia',
            'fiat': 'fiat', 'ford': 'ford', 'honda': 'honda', 'hyundai': 'hyundai', 'kia': 'kia',
            'lancia': 'lancia', 'land': 'land rover', 'mazda': 'mazda', 'mini': 'mini',
            'nissan': 'nissan', 'opel': 'opel', 'peugeot': 'peugeot', 'renault': 'renault',
            'saab': 'saab', 'seat': 'seat', 'skoda': 'skoda', 'smart': 'smart', 'subaru': 'subaru',
            'suzuki': 'suzuki', 'toyota': 'toyota', 'volkswagen': 'volkswagen',
            'volvo': 'volvo', 'vw': 'volkswagen'
        }

    def __contains__(self, key):
        return key in self.brands

    def __getitem__(self, key):
        return self.brands[key]