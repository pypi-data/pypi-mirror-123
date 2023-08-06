from bs4 import BeautifulSoup


class Tag2Bio:
    """ Class responsible converting tag format annottated text
    to BIO format annottated text 
    
    Attributes:
        text (str): The text that will be converted 
    
    """

    def __init__(self, text: str='') -> None:
        self.text: str = text
        self.soup: BeautifulSoup = BeautifulSoup(
            self.text,
            features='html.parser'
        )
        self.parsed_text: str = ''

    def parse(self) -> str:
        """ Function to parse text from tag format to BIO format
        
        Args: 
            None
        
        Returns: 
            str: parsed text in BIO format
    
        """
        
        clean_text: str = self.soup.get_text()
        # It's a long story...
        clean_text = clean_text.replace('.', ' .')
        
        clean_text_split: list = clean_text.split()
        aux_structure: list = [['O', '']] * len(clean_text.split())
        tag_infos: list = [
            (''.join(tag.find_all(text=True)), tag.name) 
            for tag in self.soup.find_all()
        ]

        for txt_to_search, tag_name in tag_infos:
            token_qty: int = len(txt_to_search.split())
            for idx in range(len(clean_text_split) - token_qty+1):
                if clean_text_split[idx : idx+token_qty] == txt_to_search.split():
                    aux_structure[idx] = ['B', tag_name]
                    aux_structure[idx+1 : idx+token_qty] = [['I', tag_name]] * (token_qty-1) 
                    break
        
        for token, (bio_tag, tag_name) in zip(clean_text_split, aux_structure):
            separator = '-' if bio_tag != 'O' else ' '
            self.parsed_text += f'{token} {bio_tag}{separator}{tag_name.lower()}\n'

        return self.parsed_text


    def save(self, path: str='./bio_output.txt') -> None:
        """ Function to save the parsed text to a file
        
        Args: 
            path (str): path where the file will be saved
        
        Returns: 
            None
    
        """
        
        with open(path, 'w') as f:
            f.write(self.parsed_text)