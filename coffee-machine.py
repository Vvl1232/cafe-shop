import streamlit as st

# Initialize session state if it doesn't exist
if 'resources' not in st.session_state:
    st.session_state.resources = {"water": 600, "milk": 400, "coffee": 200, "tea_leaves": 100, "chocolate": 100}

menu = {
    "espresso": {"ingredients": {"water": 30, "coffee": 14}, "cost": 150},
    "latte": {"ingredients": {"water": 80, "milk": 120, "coffee": 18}, "cost": 200},
    "cappuccino": {"ingredients": {"water": 100, "milk": 80, "coffee": 14}, "cost": 250},
    "tea": {"ingredients": {"water": 150, "tea_leaves": 8}, "cost": 100},
    "hot_chocolate": {"ingredients": {"milk": 200, "chocolate": 30}, "cost": 200},
    "sandwich": {"cost": 100},
    "cake": {"cost": 150},
    "cookies": {"cost": 50}
}

# Display options to the user
st.markdown("# ☕ Coffee Machine with Snacks 🍪")
choice = st.selectbox(
    "What would you like to do today? 😄",
    ["Choose...", "View Menu 📋", "Order Treats 🛍️", "Check Resources 🛠️", "Exit 👋"]
)

# Provide information when "Choose..." is selected
if choice == "Choose...":
    st.subheader("👋 Welcome to the Coffee Machine!")
    st.info(
        "Order various types of coffee drinks such as espresso, latte, and cappuccino, "
        "along with snacks like sandwiches, cake, and cookies. You can also check resources!"
    )

elif choice == "View Menu 📋":
    st.header("☕ Drinks & Snacks Menu")
    for item in menu:
        if "ingredients" in menu[item]:
            st.header(f"**{item.capitalize()}:** {menu[item]['cost']}rs")
            st.subheader("🔸 Ingredients:")
            for ingredient in menu[item]['ingredients']:
                st.write(f"- {ingredient.capitalize()}: {menu[item]['ingredients'][ingredient]}ml/g")
            st.markdown("---")  # Separator
        else:
            st.subheader(f"**{item.capitalize()}:** {menu[item]['cost']}rs")

elif choice == "Order Treats 🛍️":
    st.header("🛍️ Place Your Order")
    
    # Allow users to select multiple items
    selected_items = st.multiselect("Select your favorite treats:", list(menu.keys()))
    
    if selected_items:
        total_cost = 0
        sufficient_resources = True
        resource_usage = {key: 0 for key in st.session_state.resources}

        # Calculate total cost and check resources
        for item in selected_items:
            if "ingredients" in menu[item]:
                for ingredient, amount in menu[item]["ingredients"].items():
                    resource_usage[ingredient] += amount
                    if resource_usage[ingredient] > st.session_state.resources[ingredient]:
                        sufficient_resources = False
                        st.error(f"❌ Not enough {ingredient} for {item}.")
                        break
            total_cost += menu[item]["cost"]

        # Display the total cost
        if sufficient_resources:
            st.success(f"✅ Total cost: {total_cost}rs")
            coins = st.text_input(f"🪙 Please pay {total_cost}rs:", "0")
            if coins.strip().isdigit() and int(coins) == total_cost:
                if st.button("💳 Pay Now"):
                    # Deduct resources
                    for item in selected_items:
                        if "ingredients" in menu[item]:
                            for ingredient, amount in menu[item]["ingredients"].items():
                                st.session_state.resources[ingredient] -= amount
                    st.success(f"🎉 Your treats are ready! Enjoy! 🍴")
            else:
                st.error("❗ Please enter the correct amount.")
        else:
            st.error("❌ Unable to process the order due to insufficient resources.")

elif choice == "Check Resources 🛠️":
    st.subheader("📊 Current Resources")
    for resource in st.session_state.resources:
        st.write(f"- {resource.capitalize()}: {st.session_state.resources[resource]}ml/g")
    st.markdown("💡 Use resources wisely to enjoy more treats!")
    
elif choice == "Exit 👋":
    st.balloons()  # Fun animation
    st.success("Thank you for visiting! Have a great day ahead! 🌟")

else:
    st.error("❌ Invalid input, please try again.")
