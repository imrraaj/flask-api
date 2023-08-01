from models.models import *

def create_email_body(reward_type: RewardType, user_obj: User, reward_obj:Reward):
    if reward_type == RewardType.DEFAULT:
        return default_reward(user_obj, reward_obj)
    if reward_type == RewardType.BIRTHDAY:
        return birthday_reward(user_obj, reward_obj)

def default_reward(user_obj, reward_obj):
    return ("Exclusive Discount Coupon - Celebrate Your Purchase!", f"""

    Dear {user_obj.name},

        We hope this email finds you well and that you've been enjoying your shopping experience with us! As a token of our appreciation for your valued patronage, we are thrilled to offer you an exciting discount coupon on your next purchase. 
        To avail this fantastic offer, simply make a purchase worth INR 5000 or more, and you'll receive a whopping {reward_obj.discount_percentage}% discount on your entire order! This exclusive deal is our way of saying thank you for being a valued customer.
        
        Your unique discount code is: <b>{reward_obj.custom_code}<b>
        
        Hurry, this offer is only valid for a limited time. Visit our website or app to browse our wide range of products and make the most of this special discount.
        Remember, your satisfaction is our priority, and we look forward to serving you with top-notch products and excellent customer service.

        Thank you for being a part of our community and happy shopping!

    Best regards,
    Storefront Team
""")


def birthday_reward(user_obj, reward_obj):
    return ("Happy Birthday! Here's a Special Gift for You 🎉",f"""

    Dear {user_obj.name},

        Wishing you a very happy birthday filled with joy and wonderful moments! On this special day, we would like to extend our warmest birthday greetings and express our gratitude for being a valued member of our community.
        To make your birthday celebration even more special, we have a surprise gift for you! As a token of our appreciation, we are delighted to offer you an exclusive birthday discount coupon.
            
        Use the coupon code ${reward_obj.custom_code} during checkout, and you will receive a fantastic {reward_obj.discount_percentage}% discount on your next purchase. Treat yourself to your favorite products and enjoy incredible savings on us!
        This offer is valid until {reward_obj.expiry_date}, so don't miss out on this wonderful opportunity to make your birthday month unforgettable with some delightful shopping.
        From all of us at Storefront, we wish you a day filled with happiness, laughter, and cherished memories.
        Once again, happy birthday, and thank you for being a valued part of our family!

    Warm regards,
    The Storefront Team
""")
