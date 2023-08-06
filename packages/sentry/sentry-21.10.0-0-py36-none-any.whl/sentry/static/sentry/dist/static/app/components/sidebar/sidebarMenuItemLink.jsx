Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const SidebarMenuItemLink = (_a) => {
    var { to, href } = _a, props = (0, tslib_1.__rest)(_a, ["to", "href"]);
    if (href) {
        return <externalLink_1.default href={href} {...props}/>;
    }
    if (to) {
        return <link_1.default to={to} {...props}/>;
    }
    return <div tabIndex={0} {...props}/>;
};
exports.default = SidebarMenuItemLink;
//# sourceMappingURL=sidebarMenuItemLink.jsx.map