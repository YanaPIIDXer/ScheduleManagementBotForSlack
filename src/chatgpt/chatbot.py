from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class ChatBot:
    """チャットボットクラス

    ChatGPTを使ったチャットボットクラス

    Attributes:
    None yet.

    Methods:
    __init__: コンストラクタ
    """
    def __init__(self, api_key, temperature = 0.5):
        """コンストラクタ

        Args:
            api_key(str): OpenAI APIキー
            temperature(float): OpenAI APIの温度パラメータ
        """

        self.__client = OpenAI(openai_api_key=api_key, temperature=temperature)

    def set_simple_template(self, template_text, input_variables=[]):
        """シンプルなテンプレートをセット

        Args:
            template_text(str): テンプレートのテキスト
            input_variables(Array<str>): 変数リスト
        """
        prompt = PromptTemplate(template=template_text, input_variables=input_variables)
        self.__chain = LLMChain(llm=self.__client, prompt=prompt)

    def run(self, inputs={}):
        """実行

        Args
            inputs(Dic<str, str>): 変数とバインドした値
        Returns
            応答結果
        """
        if self.__chain == None: raise ValueError("Please call any methods for set template.")
        prediction = self.__chain.run(inputs)
        return prediction.strip()
    