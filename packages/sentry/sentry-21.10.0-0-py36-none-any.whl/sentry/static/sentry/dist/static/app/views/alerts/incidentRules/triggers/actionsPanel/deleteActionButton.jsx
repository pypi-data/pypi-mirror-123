Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
function DeleteActionButton(props) {
    const handleClick = (e) => {
        const { triggerIndex, index, onClick } = props;
        onClick(triggerIndex, index, e);
    };
    return (<button_1.default type="button" size="small" icon={<icons_1.IconDelete size="xs"/>} aria-label={(0, locale_1.t)('Remove action')} {...props} onClick={handleClick}/>);
}
exports.default = DeleteActionButton;
//# sourceMappingURL=deleteActionButton.jsx.map