class Bio2Tag:
    """ Class responsible converting tag format annotated text
    to BIO format annotated text 
    
    Attributes:
        text (str): The text that will be converted 
    
    """  

    def __init__(self, text: str='') -> None:
        self.text: str = text
        self.parsed_text: str = ''

    def _prepare_token(self, token_list: list) -> list:        
        """ Private function to handle the BIO formatting
        
        Args: 
            token_list (list): list of BIO token lines
        
        Returns: 
            list: list of ready to print tokens
        
        """

        prepared_token_list = list()
        len_token_list = len(token_list)

        for i, token in enumerate(token_list):
        
            token_split = token.split(' ')
            next_token = ['', ''] if i == len_token_list-1 else token_list[i+1].split(' ')

            if len(token_split) < 2:
                prepared_token_list.append(token_split[0])
            elif token_split[1][0] == 'B' and next_token[1][0] == 'I':
                prepared_token_list.append(f'<{token_split[1][2:]}> {token_split[0]}') 
            elif  token_split[1][0] == 'I' and next_token[1][0] != 'I':
                prepared_token_list.append(f'{token_split[0]} </{token_split[1][2:]}>')
            elif token_split[1][0] == 'B' and next_token[1][0] != 'I':
                prepared_token_list.append(f'<{token_split[1][2:]}> {token_split[0]} </{token_split[1][2:]}>')
            else:
                prepared_token_list.append(token_split[0])

        return prepared_token_list

    def parse(self) -> str:
        """ Function to parse text from BIO format to tag format
        
        Args: 
            None
        
        Returns: 
            str: parsed text in tag format
    
        """
        
        splitted_text = self.text.split('\n')
        self.parsed_text = ' '.join(self._prepare_token(splitted_text))

        return self.parsed_text
    
    def save(self, path: str='./tag_output.txt') -> None:
        """ Function to save the parsed text to a file
        
        Args: 
            path (str): path where the file will be saved
        
        Returns: 
            None

        """
        
        with open(path, 'w') as f:
            f.write(self.parsed_text)