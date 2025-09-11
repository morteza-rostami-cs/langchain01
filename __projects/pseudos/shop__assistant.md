<!--

# ai shopping assistant:
==

# define:

# features:
  # greeting the customer
  # ask questions to find out what she wants?
    # if exact product is not clear, keep asking more questions , until it is clear
  # then search the inventory
  # then recommend a list of products:
    product:
      # name
      # price
      # discount
      # in stock
      # some description

      # options:
        # add to cart

  # options:
    # back to shop (main) => start over

# cart:
  # a list of items
    # price and count
    # remove item
    # inc/dec more of product
  # total

# when user add to this card => send a fake notification for now!
# for the initial MVP:
  # focus on a text-based version input/print terminal
  # focus on business logic, no api no database, use json for storage
  # i want to code the business logic and Entities in a extendable way => so later api routes/controllers can consume the business logic => without any change in business code.
  # also: i can swap JSON for a db and add other things like: telegram interface, and web vueJs interface and so on...
  # i want to write the code based on: OOP, design patterns and SOLID.
  # now: first i want to write some pseudo code that sketches the whole system => in just one file.
  # use some python like syntax

  # for business logic, we need python, and ollama/llm and langchain and any other necessary pip package. but: i want to focus on pseudo code => so basically: i don't really want 100% accurate langchain or python code! we are just designing the system, so as long as later on i can look at my pseudo code, and i am like: ah , i need to implement langchain_rag in the class and this is how to connect it to the whole system , then we are good!!

  # so: now i want you to go head and generate a list of atomic tasks, that if i finish one by one! i have the complete pseudo code for the mvp!! with OOP and design patterns in mind!! and all in one page!
  # then i past back each task into GPT and i do them one by one!


 -->

<!--

# for telegram => use chat id
# for wen => use cookie or something

# use a session_id in terminal-based app
session_id = "guest"

class User:
  constructor(self, id: str, name: str = "Guest"):
    self.id = id
    self.name = name

#=======================================

class Product:

  constructor(self, id: str, name: str, description: str, price: float, discount: float=0.0, stock: int=0):
    self.id = id
    self.name = name
    self.description = description
    self.price = price
    # percent 0.10 for 10%
    self.discount = discount
    self.stock = stock

  def final_price(self) -> float:
    """ calculate the price after discount """
    return self.price * (1 - self.discount)

  def is_in_stock(self) -> bool:
    """ check if product is available """
    return self.stock > 0

  def __str__(self) -> str:
    """ string representation to display to user """
    return f"{self.name} - ${self.final_price():.2f} (stock: {self.stock}, discount: {self.discount*100:.0f}%)"

#=======================================

class CartItem:

  constructor(self, product: Product, quantity: int=1):
    self.product = product
    self.quantity = quantity

  def increase(self, amount: int = 1):
    """ increase quantity of this product in the cart """
    self.quantity += amount

  def decrease(self, amount: int =1):
    """ decrease quantity (cant go below 1) """
    self.quantity = max(1, self.quantity - amount)

  def subtotal(self) -> float:
    """ calc final price * quantity """
    return self.product.final_price() * self.quantity

  def __str__(self) -> str:
    return f"{self.product.name} x{self.quantity} {self.subtotal()}"

#=======================================

class Cart:

  constructor(self):
    self.items: list[CartItem] = []

  def add_item(self, product: Product, quantity: int=1):
    """
    add a product to the cart
    if product already in the cart => increase it quantity
    """

    for item in self.items:
      if item.product.id == product.id:
        item.increase(quantity)
        return

    # if product not in cart.items
    self.items.append(CartItem(product, quantity))

  def remove_item(self, product_id: str):
    """ remove an item from the cart """
    self.items = [item for item in self.items if item.product.id != product_id]

  def total_price(self) -> float:
    """ calc total cost of all items in the cart """
    return sum(item.subtotal() for item in self.items)

  def list_items(self) -> str:
    """ return a list of cart items """

    # just return a list
    return self.items

  def clear(self):
    """ empty the cart """
    self.items = []

#=======================================

class Inventory:

  constructor(self, storage: IStorage):
    """
    Inventory depends on IStorage (not JSON directly)
    this allows swapping (JsonStorage, DbStorage, etc...)
    """

    self.storage = storage
    self.products: list[Product] = self.storage.load_products()

  def get_by_id(self, product_id: str) -> Product | None:
    """
    get a product by id
    """

    for product in self.products:
      if product.id == product_id:
        return product

    return None

  ⁉️⁉️⁉️⁉️⁉️⁉️⁉️⁉️⁉️⁉️
  def search(self, query: str) -> list[Product]:
    """
    simple search by name/description (can later use ai ranking)
    """

    query = query.lower()

    results = [
      product for product in self.products
      if query in product.name.lower() or query in product.description.lower()
    ]

    return results

  def list_all(self) -> list[Product]:
    """ return all products """

    return self.products

#=======================================

# interface for storage

class IStorage(ABC):

  @abstractmethod
  def load_products(self) -> list[Product]:
    """ load products from storage """
    pass

  @abstractmethod
  def save_cart(self, user_id: str, cart: Cart):
    """ save cart to storage """
    pass

  @abstractmethod
  def load_cart(self, user_id: str) -> Cart:
    """ load cart from a storage """
    pass

#=======================================

class JsonStorage(IStorage):
  """ concrete json storage """

  constructor(self, products_file: str, carts_file: str):
    # file for products and for cart
    self.products_file = products_file
    self.carts_file = carts_file

  def load_products(self) -> list[Product]:
    """
    load products from a json file
    """

    with open(self.products_file, "r") as file:
      data = json.load(f)

    return [Product(**p) for p in data]

  def save_cart(self, user_id: str, cart: Cart):
    """ save user's cart into json (keyed by user_id) """

    try:

      with open(self.carts_file, 'r') as file:
        carts_data = json.load(file)

    except FileNotFoundError:
      carts_data = {}

    # add all cart.items
    carts_data[user_id] = [
      {"product_id": item.product.id, "quantity": item.quantity}
      for item in cart.items
    ]

    # write back into JSON
    with open(self.carts_file, "w") as file:
      json.dump(carts_data, file, indent=2)

  def load_cart(self, user_id: str) -> Cart:
    """ load user cart from json => session-based """
    try:
      with open(self.carts_file) as file:
        carts_data = json.load(file)

    except FileNotFoundError:
      carts_data = {}

    # load a single cart based on user_id (session)
    cart = Cart()

    if user_id in carts_data:
      """
      carts_data: {"user-1": [{product_id: 1, quantity: 2}, {}]}

      """
      cart_items = carts_data[user_id]

      if not len(cart_items):
        print(f"cart for user: {user_id} was not found")
        return cart

      for entry in cart_items:
        # get each product => out of json.cart.data {"product_id": "1", "quantity": "2"}

        product = self.find_product(product_id=entry["product_id"])

        if product:
          # add an item/quantity to cart
          cart.add_item(product, entry["quantity"])

    return cart

  def find_product(self, product_id: str) -> Product | None:
    """
    utility method to find a Product in products file
    """

    products = self.load_products()

    for p in products:
      if p.id == product_id:
        return p

    return None

#=======================================



class IClarificationEngine(ABC):
  @abstractmethod
  def detect_intent(self, user_input: str) -> dict:
    """
    return json: {
      intent: "shopping" | "other",
      category: "shirt" | None
    }
    """
    pass

  @abstractmethod
  def decide_required_fields(self, category: str) -> list[str]:
    """
    return a list of 4 required fields for given category.
    """
    pass

  @abstractmethod
  def clarify_fields(self, category: str, user_input: str) -> dict:
    """
    perform one llm-driven clarification step.
    return json with keys:
      - status: "incomplete" | "complete"
      - collected_data: dict (new extracted fields) eg: color, budget
      - missing_fields: list[str]
      # if: incomplete => it returns the next question
      - question: str
    """
    pass



#=======================================

class LangChainClarificationEngine(IClarificationEngine):

  constructor(self, llm):
    # could be ollama , openai etc...
    self.llm = llm

  def detect_intent(self, user_input: str) -> dict:
    prompt = f"""
    User message: {user_input}
    Determine if this is a shopping request.
    Return JSON with keys: intent ("shopping" or "other"), category (if any).
    """

    response = self.llm.predict(prompt)
    return json.loads(response)

  def decide_required_fields(self, category: str) -> list:
    """
    - you can declare pre_defined fields for each category. eg: shirt:{size, color, budget}
    or let llm some how define fields based on each category
    """

    prompt = f"""
    For category "{category}", suggest up to 4 product attributes
    that are necessary to recommend a product (return JSON array).
    Example: ["size","color","budget"]
    """

    raw = self.llm.predict(prompt)

    try:
      fields = json.loads(raw)
      if isinstance(fields, list) and fields:
        return fields[:4]

    except Exception as e:
      print e

    #ultimate fallback
    return ["budget"]

    def clarify_step(self, collected: dict, last_user_input: str) -> dict:
      """
      ask questions and fill up the fields.
      return strict json (status, collected_data, missing_fields, question)
      """

      required = self.decide_required_fields(collected.get('category', ""))

      prompt = F"""
        your are a shopping assistant.

        collected data so far:
        {json.dumps(collected)}

        required fields for category: {collected.get("category")} are:
        {json.dumps(required)}

        user last said: {last_user_input}

        return JSON ONLY with:
        {{
          "status": "incomplete" or "complete",
          "collected_data": {{...}} # fields you've extracted or updated
          "missing_fields": [...], # list of still-missing fields
          "question": "next question to ask the user (if incomplete)"
        }}
        If you can fill all required fields from the user input, set status=complete.
        Ask only ONE follow-up question when incomplete.
      """

      raw = self.llm.predict(prompt)
      return json.loads(raw)


#=======================================

class ClarificationService:
  """
  handles multi-step prompt/chain LLM
  """

  constructor(
    self,
    recommend_service: RecommendationService,
    clarifier: IClarificationEngine,
  ):
    self.recommend_service = recommend_service
    self.clarifier = clarifier

  def run(self, init_input: str) -> list:

    # step 1
    intent_info = self.clarifier.detect_intent(init_input)

    if intent_info.get("intent") != "shopping":
      return {
        "error": "not_shopping",
        message: "I can only help you with shopping"
      }

    # get category -> shirt
    category = intent_info.get("category", "general")

    collected = {
      category: category,
    }

    # step 2
    # shirt => what are required fields? size, color etc... (work on the exact algo)
    required_fields = self.clarifier.decide_required_fields(init_input)

    # step 3:
    # clarification loop => keep calling llm => until status = complete

    last_input = init_input
    while True:
      step = self.clarifier.clarify_step(collected, last_input)

      # merge new data => from last llm call
      collected.update(step.get("collected_data", {}))

      if step.get("status") == "complete":
        # step 4: return filters

        return {
          status: "ok",
          filters: collected
        }

      # if not complete => keep asking question
      question = step.get("question", "can you clarify?")
      last_input = input(f"{question} >")

#=======================================

# recommendation engine interface => so we can have different recommendation systems

class IRecommendationEngine(ABC):
  @abstractmethod
  def recommend(self, query: str, products: List[Product]) -> List[Product]:
    """ given a query/filters + products => return ranked products """
    pass

#=======================================

# simple keyword-based recommendation

class SimpleKeywordEngine(IRecommendationEngine):

  def recommend(self, query: str, products: List[Product]) -> List[Product]:

    # user query
    query = query.lower()

    # super simple word search
    # exact match in product.name => 10 score
    # match in product.description => 5 score

    ranked = []

    for product in products:
      score = 0

      if query in product.name.lower():
        score += 10

      if query in product.description.lower():
        score += 5

      if score > 0:
        # if query was found => push into ranked products
        ranked.append((score, product))

    # sort by score: highest first
    ranked.sort(key=lambda x: x[0], reverse=True)

    # skip score -> only grab product
    return [p for _, p in ranked]

#=======================================

class LangChainRecommendEngine(IRecommendationEngine):

  def recommend(filters: list[str], query: str, products):
    pass

#=======================================

# now we use service wrapper => so we can use different recommendation engines, Simple, Langchain and etc..

class RecommendationService:

  constructor(self, engine: IRecommendationEngine):
    self.engine = engine

  def recommend_products(
    self,
    query: str="",
    filters: list[any]=None,
    products: List[Product]

  ) -> list[Product]:
    """ recommend products using selected engine """
    return self.engine.recommend(filters, query, products)

#=======================================

# facade/service layer

class ShopService:

  constructor(
    self,
    inventory: Inventory,
    recommend_service: RecommendationService,
    clarifier_service: ClarificationService,
    notifier_service: INotifier,
  ):
    self.inventory = inventory
    self.notifier_service = notifier_service
    self.recommend_service = recommend_service
    self.clarifier_service = clarifier_service

    self.user_id = "guest"

    # create a cart per session
    self.card = Cart()

  def greet(self):
    """ greeting the customer """
    print("👋 welcome to shop!")
    print("you can search for products! eg: 'headphone'")

  def handle_customer(self, user_input: str):
    """
    high-level: orchestrates the whole flow of clarifying and recommending
    """
    filters = self.clarifier_service.run(user_input)

    recommendations = self.recommend_service.recommend_products(filters)

    if isinstance(recommendations, str):
      # message: your query was non-shopping
      print(recommendations)
      return recommendations # str
    else:
      return recommendations # list

  # -------------cart handling

  def add_to_cart(self, product: Product, quantity: int=1):
    self.cart.add_item(product, quantity)
    print ✅ added {quantity} x {product.name} to your cart.

    self.notifier_service.notify(self.user_id, f"added {product.name} ro cart")

  def remove_from_cart(self, product_id: str):
    self.cart.remove_item(product_id)
    print(f"🗑️ Removed product {product_id} from your cart.")

  def show_cart(self):
    print("🛒 Your Cart:")
    for item in self.cart.list_items():
      print(f"- {item.product.name} x {item.quantity} = ${item.subtotal()}")
    print(f"💰 Total = ${self.cart.total_price()}")

#=======================================

class TerminalUI:

  constructor(self, shop_service: ShopService):
    self.shop = shop_service

  def run():
    """
    run the program they way that user sees shit inside the terminal
    """

    shop.greet()

    # main terminal UI loop
    while True:
      self.show_main_menu()

      choice = input("choose option: ").strip()

      if choice == "1":
        self.handle_shopping()
      elif choice == "2":
        self.handle_cart()

      elif choice == "3":
        print "bye"
        break

      else:
        print "Invalid option."

  def show_main_menu(self):
    """ print main menu options """
    print("1. 🛍️ Shop products")
    print("2. 🛒 View cart")
    print("3. ❌ Exit")

  def handle_shopping(self, user_input: str):
    query = input("what do you want to buy?, /exit")

    if query.lower() == "/exit":
      print("Bye!")
      continue

    recommendations = shop.handle_customer(user_input=user_input)

    print("\n Recommended products: \n")

    # just print a list of products
    for i, product int enumerate(recommendations, start=1):
      print {i} {product.name} - {product.price} {product.description}

    # pick a product to add to card
    choice = input("select a product number to add to cart OR /back")

    if choice.lower() == "/back":
      print("back to main menu\n")
      continue

    if choice.isdigit() and 1 <= int(choice) <= len(recommendations):
      product = recommendations[int(choice) - 1] # starting from index 0

      self.shop.add_to_cart(product)

      print added {product.name} to cart

  def handle_cart(self):
    """ show, add, remove, inc, dec from cart """

    cart = self.shop.view_cart()

    # empty cart
    if not cart.items:
      print("🛒 Your cart is empty.")
      return

    print "\n your cart: \n"

    # print cart elements
    for i, (item, qty) in enumerate(cart.items.items(), start=1):
      print {i}: {item.name} x{qty} - {item.price * qty}

    # cart actions

    print("Options: [i]ncrease, [d]ecrease, [r]emove, [b]ack")
    cmd = input("Choose action: ").strip().lower()

    if cmd.lower() == '/back':
      print('back to main menu: \n')
      continue

    if cmd in ["i", "d", "r"]:
      # enter item number:
      idx = int(input("Enter item number: \n").strip())

      product = list(cart.items.keys())[idx-1]

      if cmd == "i":
        self.shop.inc_item(product)
      elif cmd == "d":
        self.shop.dec_item(product)
      elif cmd == "r":
        self.shop.remove_item(product)

#=======================================

class INotifier(ABC):
  @abstractmethod
  def notify(self, user_id: str, message: str):
    """ send notification message to admin, telegram etc """
    pass

#=======================================

class FakeNotifier(INotifier):
  def notify(self, user_id: str, message: str):
    print [notify] user {user_id} {message}

#=======================================
#=======================================
#=======================================
#=======================================
#=======================================
#=======================================
#=======================================
#=======================================
#=======================================
#=======================================
#=======================================
#=======================================
#=======================================
#=======================================

















# examples

storage = JsonStorage(
  products_file="products.json",
  carts_file="carts.json"
)

inventory = Inventory(storage=storage)

products = inventory.list_all()

results = inventory.search("headphones")

#----------------------------

engine = SimpleKeywordEngine()

recommend_service = RecommendationService(service)

shop = ShopService(inventory, recommend_service)

query = shop.ask_until_clear()
results = shop.recommend_products(query)



query = "headphone"
results = recommend_service.recommend_products(query, inventory.list_all())

#----------------------------
#----------------------------







 -->
