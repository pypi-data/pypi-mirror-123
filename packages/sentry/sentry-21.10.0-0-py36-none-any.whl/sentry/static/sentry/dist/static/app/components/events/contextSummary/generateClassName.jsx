Object.defineProperty(exports, "__esModule", { value: true });
const utils_1 = require("app/utils");
function generateClassname(name, version) {
    if (!(0, utils_1.defined)(name)) {
        return '';
    }
    const lowerCaseName = name.toLowerCase();
    // amazon fire tv device id changes with version: AFTT, AFTN, AFTS, AFTA, AFTVA (alexa), ...
    if (lowerCaseName.startsWith('aft')) {
        return 'amazon';
    }
    if (lowerCaseName.startsWith('sm-') || lowerCaseName.startsWith('st-')) {
        return 'samsung';
    }
    if (lowerCaseName.startsWith('moto')) {
        return 'motorola';
    }
    if (lowerCaseName.startsWith('pixel')) {
        return 'google';
    }
    const formattedName = name
        .split(/\d/)[0]
        .toLowerCase()
        .replace(/[^a-z0-9\-]+/g, '-')
        .replace(/\-+$/, '')
        .replace(/^\-+/, '');
    if (formattedName === 'edge' && version) {
        const majorVersion = version.split('.')[0];
        const isLegacyEdge = majorVersion >= '12' && majorVersion <= '18';
        if (isLegacyEdge) {
            return 'legacy-edge';
        }
    }
    return formattedName;
}
exports.default = generateClassname;
//# sourceMappingURL=generateClassName.jsx.map