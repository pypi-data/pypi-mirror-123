Object.defineProperty(exports, "__esModule", { value: true });
const locale_1 = require("app/locale");
const styles_1 = require("./styles");
const Header = () => (<styles_1.Grid>
    <styles_1.GridCell>{(0, locale_1.t)('Id')}</styles_1.GridCell>
    <styles_1.GridCell>{(0, locale_1.t)('Name')}</styles_1.GridCell>
    <styles_1.GridCell>{(0, locale_1.t)('Label')}</styles_1.GridCell>
    <styles_1.GridCell>{(0, locale_1.t)('Filename')}</styles_1.GridCell>
    <styles_1.GridCell>{(0, locale_1.t)('Status')}</styles_1.GridCell>
  </styles_1.Grid>);
exports.default = Header;
//# sourceMappingURL=header.jsx.map