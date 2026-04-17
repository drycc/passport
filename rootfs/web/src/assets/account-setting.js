const fs = require('fs');
const content = fs.readFileSync('/home/duanhongyi/Sources/passport/rootfs/web/src/views/AccountSetting.vue', 'utf8');

const regex = /<style lang="css" scoped>[\s\S]*<\/style>/g;
const newContent = content.replace(regex, '<style scoped>\n/* Removed legacy styles */\n</style>');

// We also need to rewrite the template part to use tailwind classes.

