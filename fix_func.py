with open('e:/vibecode/sillytavern-image-gen/index.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 4885 is corrupted: log(`Failed to load presets: ${e.message}
# It's missing `); } closing the catch block
# Fix it

for i, line in enumerate(lines):
    if i >= 4880 and i <= 4925:
        print(f'{i+1}: {line}', end='')

# Fix line 4885 (index 4884): add missing `);
#     }` to close the catch block, and remove the embedded function
old_line = lines[4884]  # 0-indexed
print(f'\nLine 4885 before: {repr(old_line)}')

# The fix: 
lines[4884] = '        log(`Failed to load presets: ${e.message}`);\n'
# Now we need to remove the embedded updateLLMOverrideRouteInfo from inside populatePresetList
# Find the closing } of populatePresetList (which is now at line 4920)
# And move updateLLMOverrideRouteInfo outside

# After line 4884 fix, we have:
# 4885:     }  (catch close)
# 4886: }  (function close)
# 4887: (blank)
# 4888: function updateLLMOverrideRouteInfo() {  -- but this is INSIDE populatePresetList still
# We need to: close populatePresetList properly, then define updateLLMOverrideRouteInfo outside

# Let's rebuild this section properly
# Lines up to 4883 are fine (the for loop and try/catch)
# We need to add:
#     } catch (e) {
#         log(`Failed to load presets: ${e.message}`);
#     }
# }
# 
# function updateLLMOverrideRouteInfo() {
#     ... (lines 4888-4920)
# }

# Find where the real updateLLMOverrideRouteInfo ends (after line 4920)
# Find getResolvedLLMPrefill
for i in range(4920, 4940):
    if 'getResolvedLLMPrefill' in lines[i]:
        print(f'{i+1}: {lines[i]}', end='')
        break

# After line 4920 there should be blank line, then getResolvedLLMPrefill
# Let's rebuild from line 4883

# Keep lines 0-4883 (0-indexed) as is
# Remove lines 4884-4920
# Insert corrected code

new_section = [
    '        }\n',
    '    } catch (e) {\n',
    '        log(`Failed to load presets: ${e.message}`);\n',
    '    }\n',
    '}\n',
    '\n',
    'function updateLLMOverrideRouteInfo() {\n',
    '    const s = getSettings();\n',
    '    const routeStatus = document.getElementById("qig-llm-override-route-status");\n',
    '    const routeEndpoint = document.getElementById("qig-llm-override-route-endpoint");\n',
    '    if (!routeStatus || !routeEndpoint) return;\n',
    '\n',
    '    if (!s.llmOverrideEnabled) {\n',
    '        routeStatus.innerHTML = "🔒 Запросы идут на основной AI чата";\n',
    '        routeEndpoint.textContent = "Маршрут не настроен";\n',
    '        return;\n',
    '    }\n',
    '\n',
    '    if (s.llmOverrideProfileId) {\n',
    '        let profileUrl = "";\n',
    '        try {\n',
    '            const ctx = getContext();\n',
    '            const CMRS = ctx.ConnectionManagerRequestService;\n',
    '            if (CMRS) {\n',
    '                const profile = CMRS.getProfile(s.llmOverrideProfileId);\n',
    '                profileUrl = profile?.api_url || profile?.url || profile?.endpoint || "";\n',
    '            }\n',
    '        } catch {}\n',
    '        const profileLabel = s.llmOverrideProfileId.length > 30\n',
    '            ? s.llmOverrideProfileId.substring(0, 27) + "..."\n',
    '            : s.llmOverrideProfileId;\n',
    '        routeStatus.innerHTML = "✅ Запросы идут на: " + escapeHtml(profileLabel);\n',
    '        routeEndpoint.textContent = profileUrl\n',
    '            ? ("Endpoint: " + escapeHtml(profileUrl.substring(0, 60)))\n',
    '            : "Профиль маршрутизации активен";\n',
    '    } else {\n',
    '        routeStatus.innerHTML = "⚠️ Выберите Connection Profile для активации";\n',
    '        routeEndpoint.textContent = "Профиль не выбран — запросы пойдут на основной AI чата";\n',
    '    }\n',
    '}\n',
]

# Replace lines 4884 through 4920 (0-indexed) with the new section
# Line 4884 is index 4883
lines = lines[:4883] + new_section + lines[4921:]

with open('e:/vibecode/sillytavern-image-gen/index.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('\nFixed!')