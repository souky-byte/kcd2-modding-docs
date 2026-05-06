# Random Event Node

> Source: [https://youtrack.warhorsestudios.cz/articles/KM-A-74](https://youtrack.warhorsestudios.cz/articles/KM-A-74)

*(image: )*  

A module that contains **Random event variant** nodes and possibly some common logic for the event. Acts as an event definition, to later be instanced in different event places. Should only be created in the "*Barbora/random_events*" library.

* Inputs:
  * ***OnSpawn*** — triggers when event spawns
  * ***OnDespawn*** — triggers when event despawns
* Outputs:
  * ***ActivateCooldown*** — trigger event cooldown
  * ***IsEnabled*** — bool port to disable/enable event
* Properties:
  * ***Cooldown*** — defines event cooldown
  * ***Tags*** — an array of tags that can be used later to disable event by activating the **DisableRandomEvent** node.  New tags can be defined in "*Tables\RandomEvent\RandomEventTag.xml*"
