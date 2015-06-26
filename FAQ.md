# FAQ

## Why on Earth did you make such a thing?

Well my big deal was that I wanted a configuration file format that was more expressive than INI, but less annoying that JSON. I think JSON is a fine format, but I find it irritatingly limited, and it forces me to remember things it doesn't seem like I should have to remember. Also no comments. Don't get my started on YAML - I've had so much frustration with it, I just cannot even.

I have a lot of application situations (such as my game engine PyBoop) that need configuration, and to me there's almost no point in doing a thing unless it's generic!

## But YAML is surely no worse than Python?!

Hey I don't know. Never had problems with Python, had tons of problems with YAML.

## Why not start with a JSON parser rather than rolling your own?

I certainly would have done so, but I used this as an excuse to learn Grako, the parser generator. Grako is pretty neat, but the BNF it uses is weird.

## The parser seems a bit /too/ forgiving, what's up with that?

I am not completely familiar with Grako or the proper way to structure BNFs for it. I will accept patches to make the BNF validate and explode on bad input. Right now it just seems to stop at the spot it can't parse.
