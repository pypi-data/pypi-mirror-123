Para você usar essa Api é necessário:
- Transferir todos os dados do seu inventário para um csv usando o BakkesMod.
- Baixar esse pacote pelo pip.

```
pip install rl-inventory-api
```

Essa Api tem como função principal facilitar obtenção de dados específicos de seu inventário de maneira simples,
por exemplo, imagine poder descobrir quantos itens non crate você tem:

```py
from rl_inventory_api import Inventory

inv = Inventory.read()
my_non_crate_items = inv.filter_non_crate().items
amount_of_non_crate = len(my_non_crate_items)
```
Pronto, com apenas 4 linhas de código você conseguiu obter todos os dados dos seus itens non crate e também a quantidade
de itens non-crate que você tem.