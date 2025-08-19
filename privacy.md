## Privacy Policy

This policy explains what data this Discord bot (the "Bot") accesses, collects, stores, and how it is used.

### Permissions and Intents
The Bot operates with the following Discord permissions/intents (as configured in the code and application settings):
- Guilds intent
- Messages intent 
- Message Content intent (only if explicitly enabled)
- Standard bot permissions such as: Send Messages, Embed Links, Attach Files, Read Message History 

Scopes requested on invite:
- bot
- applications.commands (for slash commands)

### Data We Collect and Store
Depending on which features you use, the Bot may store the following per-guild data:
- Server (Guild) ID and, where relevant, Channel IDs
- Dictionary entries you submit: term, definition, optional image reference, and metadata (creator user ID and nickname, created/updated timestamps)
- Usage counters for terms 

If usage monitoring is enabled by server admins, the Bot may read message content to detect term usage. Message content is processed transiently for matching; the Bot stores only aggregated counters and/or related term usage metadata, not full message bodies.

### Data Access
Data relating to definitions of terms, including the image references and metadata, is accessible by any member of the Discord guild the data was submitted in. 
The Bot maintainer is not responsible for the leakage of sensitive information submitted to the bot. As such, it is highly recommended that all information submitted should not be considered sensitive.

### How We Use the Data
- Provide dictionary functionality (store and retrieve terms/definitions)
- Generate embeds/images for definitions
- Count usage of configured terms when monitoring is enabled
- Operate slash commands and reply to users

### Data Retention
- Dictionary entries and metadata persist until removed by server admins
- Usage counters persist until cleared by server admins
- No full message content is retained beyond transient processing for monitoring

### Data Deletion (Admin Controls)
Server administrators can delete data using in-bot commands:
- /clear_data usage — clears usage data (e.g., usage counters) and may remove related monitoring configuration
- /clear_data dictionary — clears all data relating to terms and definitions
- /clear_data full — clears all stored data for the guild (terms, definitions, usage data)

If a data deletion command fails, manual deletion can be requested by contacting the Bot maintainer.


### Children’s Privacy
The Bot is intended for Discord users in accordance with Discord’s Terms of Service and age requirements. It does not knowingly collect information from children under the applicable age of digital consent.

### Changes
We may update this policy to reflect changes to functionality or compliance requirements. Continued use after changes constitutes acceptance.

### Contact
For questions or requests regarding privacy or data removal, please contact the Bot maintainer on Discord.

