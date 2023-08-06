Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const icons_1 = require("app/icons");
const fileExtension_1 = require("app/utils/fileExtension");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const FileIcon = ({ fileName, size: providedSize = 'sm', className }) => {
    var _a;
    const fileExtension = (0, fileExtension_1.getFileExtension)(fileName);
    const iconName = fileExtension ? (0, fileExtension_1.fileExtensionToPlatform)(fileExtension) : null;
    const size = (_a = theme_1.default.iconSizes[providedSize]) !== null && _a !== void 0 ? _a : providedSize;
    if (!iconName) {
        return <icons_1.IconFile size={size} className={className}/>;
    }
    return (<img src={require(`platformicons/svg/${iconName}.svg`)} width={size} height={size} className={className}/>);
};
exports.default = FileIcon;
//# sourceMappingURL=fileIcon.jsx.map