#!/usr/bin/env python3
import iterm2


async def _get_preset(connection, theme):
    if 'dark' in theme:
        return await iterm2.ColorPreset.async_get(connection, 'OneHalfDark')
    return await iterm2.ColorPreset.async_get(connection, 'OneHalfLight')


async def _set_preset(connection, preset):
    profiles = await iterm2.PartialProfile.async_query(connection)
    for profile in profiles:
        full_profile = await profile.async_get_full_profile()
        await full_profile.async_set_color_preset(preset)


async def main(connection):
    app = await iterm2.async_get_app(connection)
    theme = await app.async_get_theme()
    preset = await _get_preset(connection, theme)
    await _set_preset(connection, preset)

    async with iterm2.VariableMonitor(connection, iterm2.VariableScopes.APP, 'effectiveTheme', None) as mon:
        while True:
            e_theme = await mon.async_get()
            preset = await _get_preset(connection, e_theme)
            await _set_preset(connection, preset)


iterm2.run_forever(main)
