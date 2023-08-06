Object.defineProperty(exports, "__esModule", { value: true });
exports.SuggestedAssignees = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const actorAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/actorAvatar"));
const suggestedOwnerHovercard_1 = (0, tslib_1.__importDefault)(require("app/components/group/suggestedOwnerHovercard"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const sidebarSection_1 = (0, tslib_1.__importDefault)(require("../sidebarSection"));
const SuggestedAssignees = ({ owners, onAssign }) => (<sidebarSection_1.default title={<react_1.Fragment>
        {(0, locale_1.t)('Suggested Assignees')}
        <Subheading>{(0, locale_1.t)('Click to assign')}</Subheading>
      </react_1.Fragment>}>
    <Content>
      {owners.map((owner, i) => (<suggestedOwnerHovercard_1.default key={`${owner.actor.id}:${owner.actor.email}:${owner.actor.name}:${i}`} {...owner}>
          <actorAvatar_1.default css={(0, react_2.css) `
              cursor: pointer;
            `} onClick={onAssign(owner.actor)} hasTooltip={false} actor={owner.actor}/>
        </suggestedOwnerHovercard_1.default>))}
    </Content>
  </sidebarSection_1.default>);
exports.SuggestedAssignees = SuggestedAssignees;
const Subheading = (0, styled_1.default)('small') `
  font-size: ${p => p.theme.fontSizeExtraSmall};
  color: ${p => p.theme.gray300};
  line-height: 100%;
  font-weight: 400;
  margin-left: ${(0, space_1.default)(0.5)};
`;
const Content = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  grid-template-columns: repeat(auto-fill, 20px);
`;
//# sourceMappingURL=suggestedAssignees.jsx.map