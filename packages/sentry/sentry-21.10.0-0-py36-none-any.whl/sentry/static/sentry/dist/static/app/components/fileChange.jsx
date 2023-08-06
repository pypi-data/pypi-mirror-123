Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const avatarList_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/avatarList"));
const fileIcon_1 = (0, tslib_1.__importDefault)(require("app/components/fileIcon"));
const listGroup_1 = require("app/components/listGroup");
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const FileChange = ({ filename, authors, className }) => (<FileItem className={className}>
    <Filename>
      <StyledFileIcon fileName={filename}/>
      <textOverflow_1.default>{filename}</textOverflow_1.default>
    </Filename>
    <div>
      <avatarList_1.default users={authors} avatarSize={25} typeMembers="authors"/>
    </div>
  </FileItem>);
const FileItem = (0, styled_1.default)(listGroup_1.ListGroupItem) `
  display: flex;
  align-items: center;
  justify-content: space-between;
`;
const Filename = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  margin-right: ${(0, space_1.default)(3)};
  align-items: center;
  grid-template-columns: max-content 1fr;
`;
const StyledFileIcon = (0, styled_1.default)(fileIcon_1.default) `
  color: ${p => p.theme.gray200};
  border-radius: 3px;
`;
exports.default = FileChange;
//# sourceMappingURL=fileChange.jsx.map