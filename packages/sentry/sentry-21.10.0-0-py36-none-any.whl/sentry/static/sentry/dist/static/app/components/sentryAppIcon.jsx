Object.defineProperty(exports, "__esModule", { value: true });
exports.SentryAppIcon = void 0;
const icons_1 = require("app/icons");
const SentryAppIcon = ({ slug }) => {
    switch (slug) {
        case 'calixa':
            return <icons_1.IconCalixa size="md"/>;
        case 'clickup':
            return <icons_1.IconClickup size="md"/>;
        case 'komodor':
            return <icons_1.IconKomodor size="md"/>;
        case 'linear':
            return <icons_1.IconLinear size="md"/>;
        case 'rookout':
            return <icons_1.IconRookout size="md"/>;
        case 'shortcut':
            return <icons_1.IconShortcut size="md"/>;
        case 'spikesh':
            return <icons_1.IconSpikesh size="md"/>;
        case 'taskcall':
            return <icons_1.IconTaskcall size="md"/>;
        case 'teamwork':
            return <icons_1.IconTeamwork size="md"/>;
        default:
            return <icons_1.IconGeneric size="md"/>;
    }
};
exports.SentryAppIcon = SentryAppIcon;
//# sourceMappingURL=sentryAppIcon.jsx.map