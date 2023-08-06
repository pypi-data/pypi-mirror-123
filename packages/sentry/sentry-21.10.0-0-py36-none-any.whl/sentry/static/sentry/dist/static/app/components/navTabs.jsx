Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
function NavTabs(props) {
    const { underlined, className } = props, tabProps = (0, tslib_1.__rest)(props, ["underlined", "className"]);
    const mergedClassName = (0, classnames_1.default)('nav nav-tabs', className, {
        'border-bottom': underlined,
    });
    return <ul className={mergedClassName} {...tabProps}/>;
}
exports.default = NavTabs;
//# sourceMappingURL=navTabs.jsx.map