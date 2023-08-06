# Installing

## From source:
- `pip install git+https://github.com/editid0/IsDigit`

## From pypi:
- `pip install -U IsDigit`

<br />

# Examples
```python
from isdigit import IsDigit

digits = IsDigit(allow_floats=True, allow_ints=True)

print(digits.is_digit('1')) # returns True
print(digits.is_digit('1.0')) # returns True
print(digits.is_digit('1.0.0')) # returns False
print(digits.is_digit('x')) # returns False
```
Or, alternatively:
```python
from isdigit import IsDigit

digits = IsDigit()

print(digits.is_digit('1')) # returns True
print(digits.is_digit('1.0')) # returns False
print(digits.is_digit('1.0.0')) # returns False
print(digits.is_digit('x')) # returns False
```

# Using `discord.py` with IsDigit

<br />

## Install
<br />

### pip install
```
pip install -U IsDigit[discord]
```

### Install from repo
```
pip install git+https://github.com/editid0/IsDigit[discord]
```


## Basic Usage
##### Please do not use this code when making a bot. Read the `discord.py` [docs](http://discordpy.readthedocs.io/) instead.
###### This package is not affiliated with the `discord.py` library.
```python
from isdigit import IsDigit
from discord.ext import commands

bot = commands.Bot(command_prefix='prefix')
digits = IsDigit()

@bot.command()
async def test(ctx, arg: digits):
    await ctx.send(type(arg))

@test.error
async def test_error(ctx, error):
    await ctx.send(error)

bot.run('token')
```