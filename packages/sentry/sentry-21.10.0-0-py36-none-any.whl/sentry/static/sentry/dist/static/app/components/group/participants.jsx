Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const sidebarSection_1 = (0, tslib_1.__importDefault)(require("./sidebarSection"));
const GroupParticipants = ({ participants }) => (<sidebarSection_1.default title={(0, locale_1.tn)('%s Participant', '%s Participants', participants.length)}>
    <Faces>
      {participants.map(user => (<Face key={user.username}>
          <userAvatar_1.default size={28} user={user} hasTooltip/>
        </Face>))}
    </Faces>
  </sidebarSection_1.default>);
exports.default = GroupParticipants;
const Faces = (0, styled_1.default)('div') `
  display: flex;
  flex-wrap: wrap;
`;
const Face = (0, styled_1.default)('div') `
  margin-right: ${(0, space_1.default)(0.5)};
  margin-bottom: ${(0, space_1.default)(0.5)};
`;
//# sourceMappingURL=participants.jsx.map