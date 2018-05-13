from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fortnite_database_setup import Weapon, Base, WeaponDetail, User

engine = create_engine('sqlite:///fortniteweapondatabase.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(username="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Add AR's
ar = Weapon(user_id = 1, name = "Assault Rifles")
session.add(ar)
session.commit()

greyAR = WeaponDetail(user_id = 1, name = "Grey AR", description = "common assault rifle", color = "grey", damage = "30", weapon = ar)
session.add(greyAR)
session.commit()

greenAR = WeaponDetail(user_id = 1, name = "Green AR", description = "uncommon assault rifle", color = "green", damage = "31", weapon = ar)
session.add(greenAR)
session.commit()

blueAR = WeaponDetail(user_id = 1, name = "Blue AR", description = "rare assault rifle", color = "blue", damage = "33", weapon = ar)
session.add(blueAR)
session.commit()

purpleSCAR = WeaponDetail(user_id = 1, name = "Purple SCAR", description = "epic assault rifle", color = "purple", damage = "35", weapon = ar)
session.add(purpleSCAR)
session.commit()

goldSCAR = WeaponDetail(user_id = 1, name = "Gold SCAR", description = "legendary assault rifle", color = "gold", damage = "36", weapon = ar)
session.add(goldSCAR)
session.commit()

greyBurst = WeaponDetail(user_id = 1, name = "Grey Burst", description = "common burst assault rifle", color = "grey", damage = "27", weapon = ar)
session.add(greyBurst)
session.commit()

greenBurst = WeaponDetail(user_id = 1, name = "Green Burst", description = "uncommon burst assault rifle", color = "green", damage = "29", weapon = ar)
session.add(greenBurst)
session.commit()

blueBurst = WeaponDetail(user_id = 1, name = "Blue Burst", description = "rare burst assault rifle", color = "blue", damage = "30", weapon = ar)
session.add(blueBurst)
session.commit()

blueScopedAR = WeaponDetail(user_id = 1, name = "Blue Scoped AR", description = "rare scoped assault rifle", color = "blue", damage = "23", weapon = ar)
session.add(blueScopedAR)
session.commit()

purpleScopedAR = WeaponDetail(user_id = 1, name = "Purple Scoped AR", description = "epic scoped assault rifle", color = "purple", damage = "24", weapon = ar)
session.add(purpleScopedAR)

blueLMG = WeaponDetail(user_id = 1, name = "Blue LMG", description = "rare light machine gun", color = "blue", damage = "25", weapon = ar)
session.add(blueLMG)
session.commit()

purpleLMG = WeaponDetail(user_id = 1, name = "Purple LMG", description = "epic light machine gun", color = "purple", damage = "26", weapon = ar)
session.add(purpleLMG)
session.commit()

#Add Grenade Launchers
grenadelauncher = Weapon(user_id = 1, name = "Grenade Launchers")
session.add(grenadelauncher)
session.commit()

blueLauncher = WeaponDetail(user_id = 1, name = "Blue Grenade Launcher", description = "rare grenade launcher", color = "blue", damage = "100", weapon = grenadelauncher)
session.add(blueLauncher)
session.commit()

purpleLauncher = WeaponDetail(user_id = 1, name = "Purple Grenade Launcher", description = "epic grenade launcher", color = "purple", damage = "100", weapon = grenadelauncher)
session.add(purpleLauncher)
session.commit()

goldLauncher = WeaponDetail(user_id = 1, name = "Gold Grenade Launcher", description = "legendary grenade launcher", color = "gold", damage = "100", weapon = grenadelauncher)
session.add(goldLauncher)
session.commit()

#Add Pistols
pistol = Weapon(user_id = 1, name = "Pistols")
session.add(pistol)
session.commit()

greyRevolver = WeaponDetail(user_id = 1, name = "Grey Revolver", description = "common revolver", color = "grey", damage = "54", weapon = pistol)
session.add(greyRevolver)
session.commit()

greenRevolver = WeaponDetail(user_id = 1, name = "Green Revolver", description = "uncommon revolver", color = "green", damage = "57", weapon = pistol)
session.add(greenRevolver)
session.commit()

blueRevolver = WeaponDetail(user_id = 1, name = "Blue Revolver", description = "rare revolver", color = "blue", damage = "60", weapon = pistol)
session.add(blueRevolver)
session.commit()

greyPistol = WeaponDetail(user_id = 1, name = "Grey Pistol", description = "common pistol", color = "grey", damage = "23", weapon = pistol)
session.add(greyPistol)
session.commit()

greenPistol = WeaponDetail(user_id = 1, name = "Green Pistol", description = "uncommon pistol", color = "green", damage = "24", weapon = pistol)
session.add(greenPistol)
session.commit()

bluePistol = WeaponDetail(user_id = 1, name = "Blue Pistol", description = "rare pistol", color = "blue", damage = "25", weapon = pistol)
session.add(bluePistol)
session.commit()

purpleSuppressedPistol = WeaponDetail(user_id = 1, name = "Purple Suppressed Pistol", description = "epic pistol", color = "purple", damage = "26", weapon = pistol)
session.add(purpleSuppressedPistol)
session.commit()

goldSuppressedPistol = WeaponDetail(user_id = 1, name = "Gold Suppressed Pistol", description = "legendary pistol", color = "gold", damage = "28", weapon = pistol)
session.add(goldSuppressedPistol)
session.commit()

purpleHandCannon = WeaponDetail(user_id = 1, name = "Purple Hand Cannon", description = "epic hand cannon", color = "purple", damage = "75", weapon = pistol)
session.add(purpleHandCannon)
session.commit()

goldHandCannon = WeaponDetail(user_id = 1, name = "Gold Hand Cannon", description = "legendary hand cannon", color = "gold", damage = "78", weapon = pistol)
session.add(goldHandCannon)
session.commit()

#add Rocket Launchers
rocketlauncher = Weapon(user_id = 1, name = "Rocket Launchers")
session.add(rocketlauncher)
session.commit()

blueRocketLauncher = WeaponDetail(user_id =1, name = "Blue Rocket Launcher", description = "rare rocket launcher", color = "blue", damage = "100", weapon = rocketlauncher)
session.add(blueRocketLauncher)
session.commit()

purpleRocketLauncher = WeaponDetail(user_id =1, name = "Purple Rocket Launcher", description = "epic rocket launcher", color = "purple", damage = "100", weapon = rocketlauncher)
session.add(purpleRocketLauncher)
session.commit()

goldRocketLauncher = WeaponDetail(user_id =1, name = "Gold Rocket Launcher", description = "legendary rocket launcher", color = "gold", damage = "100", weapon = rocketlauncher)
session.add(goldRocketLauncher)
session.commit()

#add Shotguns
shotgun = Weapon(user_id = 1, name = "Shotguns")

greenPump = WeaponDetail(user_id = 1, name = "Green Pump Shotgun", description = "uncommon pump shotgun", color = "green", damage = "90", weapon = shotgun)
session.add(greenPump)
session.commit()

bluePump = WeaponDetail(user_id = 1, name = "Blue Pump Shotgun", description = "rare pump shotgun", color = "blue", damage = "95", weapon = shotgun)
session.add(bluePump)
session.commit()

greyTac = WeaponDetail(user_id = 1, name = "Grey Tactical Shotgun", description = "common tactical shotgun", color = "grey", damage = "67", weapon = shotgun)
session.add(greyTac)
session.commit()

greenTac = WeaponDetail(user_id = 1, name = "Green Tactical Shotgun", description = "uncommon tactical shotgun", color = "green", damage = "70", weapon = shotgun)
session.add(greenTac)
session.commit()

blueTac = WeaponDetail(user_id = 1, name = "Blue Tactical Shotgun", description = "rare tactical shotgun", color = "blue", damage = "74", weapon = shotgun)
session.add(blueTac)
session.commit()

purpleHeavy = WeaponDetail(user_id = 1, name = "Purple Heavy Shotgun", description = "epic heavy shotgun", color = "purple", damage = "74", weapon = shotgun)
session.add(purpleHeavy)
session.commit()

goldHeavy = WeaponDetail(user_id = 1, name = "Gold Heavy Shotgun", description = "legendary heavy shotgun", color = "gold", damage = "77", weapon = shotgun)
session.add(goldHeavy)
session.commit()

#add Snipers
sniper = Weapon(user_id = 1, name = "Sniper Rifles")

blueBolt = WeaponDetail(user_id = 1, name = "Blue Bolt Sniper Rifle", description = "rare bolt-action sniper rifle", color = "blue", damage = "105", weapon = sniper)
session.add(blueBolt)
session.commit()

purpleBolt = WeaponDetail(user_id = 1, name = "Purple Bolt Sniper Rifle", description = "epic bolt-action sniper rifle", color = "purple", damage = "110", weapon = sniper)
session.add(purpleBolt)
session.commit()

goldBolt = WeaponDetail(user_id = 1, name = "Gold Bolt Sniper Rifle", description = "legendary bolt-action sniper rifle", color = "gold", damage = "116", weapon = sniper)
session.add(goldBolt)
session.commit()

purpleSemiAuto = WeaponDetail(user_id = 1, name = "Purple Semi-Auto Sniper Rifle", description = "epic semi-auto sniper rifle", color = "purple", damage = "63", weapon = sniper)
session.add(purpleSemiAuto)
session.commit()

goldSemiAuto = WeaponDetail(user_id = 1, name = "Gold Semi-Auto Sniper Rifle", description = "legendary semi-auto sniper rifle", color = "gold", damage = "66", weapon = sniper)
session.add(goldSemiAuto)
session.commit()

greenHunting = WeaponDetail(user_id = 1, name = "Green Hunting Rifle", description = "uncommon hunting rifle", color = "green", damage = "86", weapon = sniper)
session.add(greenHunting)
session.commit()

blueHunting = WeaponDetail(user_id = 1, name = "Blue Hunting Rifle", description = "rare hunting rifle", color = "blue", damage = "90", weapon = sniper)
session.add(blueHunting)
session.commit()

#Add SMG's
smg = Weapon(user_id = 1, name = "Submachine Guns")
session.add(smg)
session.commit()

greySuppressed = WeaponDetail(user_id = 1, name = "Grey Suppressed SMG", description = "common suppressed submachine gun", color = "grey", damage = "17", weapon = smg)
session.add(greySuppressed)
session.commit()

greenSuppressed = WeaponDetail(user_id = 1, name = "Green Suppressed SMG", description = "uncommon suppressed submachine gun", color = "green", damage = "18", weapon = smg)
session.add(greenSuppressed)
session.commit()

blueSuppressed = WeaponDetail(user_id = 1, name = "Blue Suppressed SMG", description = "rare suppressed submachine gun", color = "blue", damage = "19", weapon = smg)
session.add(blueSuppressed)
session.commit()

greenTacSMG = WeaponDetail(user_id = 1, name = "Green Tactical SMG", description = "uncommon tactical submachine gun", color = "green", damage = "16", weapon = smg)
session.add(greenTacSMG)
session.commit()

blueTacSMG = WeaponDetail(user_id = 1, name = "Blue Tactical SMG", description = "rare tactical submachine gun", color = "blue", damage = "16", weapon = smg)
session.add(blueTacSMG)
session.commit()

purpleTacSMG = WeaponDetail(user_id = 1, name = "Purple Tactical SMG", description = "epic tactical submachine gun", color = "purple", damage = "16", weapon = smg)
session.add(purpleTacSMG)
session.commit()

purpleMinigun = WeaponDetail(user_id = 1, name = "Purple Minigun", description = "epic minigun", color = "purple", damage = "18", weapon = smg)
session.add(purpleMinigun)
session.commit()

goldMinigun = WeaponDetail(user_id = 1, name = "Gold Minigun", description = "epic minigun", color = "gold", damage = "19", weapon = smg)
session.add(goldMinigun)
session.commit()







print "added weapons!"
