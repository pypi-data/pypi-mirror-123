Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const author_1 = (0, tslib_1.__importDefault)(require("app/components/activity/author"));
const linkWithConfirmation_1 = (0, tslib_1.__importDefault)(require("app/components/links/linkWithConfirmation"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const editorTools_1 = (0, tslib_1.__importDefault)(require("./editorTools"));
const NoteHeader = ({ authorName, user, onEdit, onDelete }) => {
    const activeUser = configStore_1.default.get('user');
    const canEdit = activeUser && (activeUser.isSuperuser || (user === null || user === void 0 ? void 0 : user.id) === activeUser.id);
    return (<div>
      <author_1.default>{authorName}</author_1.default>
      {canEdit && (<editorTools_1.default>
          <tooltip_1.default title={(0, locale_1.t)('You can edit this comment due to your superuser status')} disabled={!activeUser.isSuperuser}>
            <Edit onClick={onEdit}>{(0, locale_1.t)('Edit')}</Edit>
          </tooltip_1.default>
          <tooltip_1.default title={(0, locale_1.t)('You can delete this comment due to your superuser status')} disabled={!activeUser.isSuperuser}>
            <linkWithConfirmation_1.default title={(0, locale_1.t)('Remove')} message={(0, locale_1.t)('Are you sure you wish to delete this comment?')} onConfirm={onDelete}>
              <Remove>{(0, locale_1.t)('Remove')}</Remove>
            </linkWithConfirmation_1.default>
          </tooltip_1.default>
        </editorTools_1.default>)}
    </div>);
};
const getActionStyle = (p) => `
  padding: 0 7px;
  color: ${p.theme.gray200};
  font-weight: normal;
`;
const Edit = (0, styled_1.default)('a') `
  ${getActionStyle};
  margin-left: 7px;

  &:hover {
    color: ${p => p.theme.gray300};
  }
`;
const Remove = (0, styled_1.default)('span') `
  ${getActionStyle};
  border-left: 1px solid ${p => p.theme.border};

  &:hover {
    color: ${p => p.theme.error};
  }
`;
exports.default = NoteHeader;
//# sourceMappingURL=header.jsx.map