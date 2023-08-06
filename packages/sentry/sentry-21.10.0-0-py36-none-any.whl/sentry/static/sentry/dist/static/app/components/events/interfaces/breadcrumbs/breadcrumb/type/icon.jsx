Object.defineProperty(exports, "__esModule", { value: true });
const icons_1 = require("app/icons");
const breadcrumbs_1 = require("app/types/breadcrumbs");
function Icon({ type }) {
    switch (type) {
        case breadcrumbs_1.BreadcrumbType.USER:
        case breadcrumbs_1.BreadcrumbType.UI:
            return <icons_1.IconUser size="xs"/>;
        case breadcrumbs_1.BreadcrumbType.NAVIGATION:
            return <icons_1.IconLocation size="xs"/>;
        case breadcrumbs_1.BreadcrumbType.DEBUG:
            return <icons_1.IconFix size="xs"/>;
        case breadcrumbs_1.BreadcrumbType.INFO:
            return <icons_1.IconInfo size="xs"/>;
        case breadcrumbs_1.BreadcrumbType.ERROR:
            return <icons_1.IconFire size="xs"/>;
        case breadcrumbs_1.BreadcrumbType.HTTP:
            return <icons_1.IconSwitch size="xs"/>;
        case breadcrumbs_1.BreadcrumbType.WARNING:
            return <icons_1.IconWarning size="xs"/>;
        case breadcrumbs_1.BreadcrumbType.QUERY:
            return <icons_1.IconStack size="xs"/>;
        case breadcrumbs_1.BreadcrumbType.SYSTEM:
            return <icons_1.IconMobile size="xs"/>;
        case breadcrumbs_1.BreadcrumbType.SESSION:
            return <icons_1.IconRefresh size="xs"/>;
        case breadcrumbs_1.BreadcrumbType.TRANSACTION:
            return <icons_1.IconSpan size="xs"/>;
        default:
            return <icons_1.IconTerminal size="xs"/>;
    }
}
exports.default = Icon;
//# sourceMappingURL=icon.jsx.map