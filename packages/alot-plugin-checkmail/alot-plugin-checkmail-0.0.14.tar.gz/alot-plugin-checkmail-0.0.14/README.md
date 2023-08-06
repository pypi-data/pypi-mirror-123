# checkmail plugin for alot

A plugin that checks mail asynchronously, giving you feedback through the process via notifications.

This plugin was mostly written to accomodate running [mbsync](https://isync.sourceforge.io/mbsync.html) from inside `alot` without being intrusive. This can be useful if you do not wish to wait for your systemd timer to execute your mail sync.

## Installation

Run the following in the environment that alot's `hooks.py` uses:

```sh
pip install --upgrade alot-plugin-checkmail
```

You may need to use `sudo` if your Python installation is owned by `root`.

## Configuration

Insert the following stanza in your `~/.config/alot/config` file:

```toml
[checkmail]
  command = '/path/to/your/binary/or/script -abc --with --any --parameters'
```

## Usage

The easiest way to include your plugin is to import it directly in the top of `hooks.py` like so:

```python
from alot_checkmail import checkmail
```

You can then invoke the command in alot by running `:checkmail`.
