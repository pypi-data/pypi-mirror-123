Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const avatar_1 = (0, tslib_1.__importDefault)(require("app/components/activity/item/avatar"));
const card_1 = (0, tslib_1.__importDefault)(require("app/components/card"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function DashboardCard({ title, detail, createdBy, renderWidgets, dateStatus, to, onEventClick, renderContextMenu, }) {
    function onClick() {
        onEventClick === null || onEventClick === void 0 ? void 0 : onEventClick();
    }
    return (<link_1.default data-test-id={`card-${title}`} onClick={onClick} to={to}>
      <StyledDashboardCard interactive>
        <CardHeader>
          <CardContent>
            <Title>{title}</Title>
            <Detail>{detail}</Detail>
          </CardContent>
          <AvatarWrapper>
            {createdBy ? (<avatar_1.default type="user" user={createdBy} size={34}/>) : (<avatar_1.default type="system" size={34}/>)}
          </AvatarWrapper>
        </CardHeader>
        <CardBody>{renderWidgets()}</CardBody>
        <CardFooter>
          <DateSelected>
            {dateStatus ? (<DateStatus>
                {(0, locale_1.t)('Created')} {dateStatus}
              </DateStatus>) : (<DateStatus />)}
          </DateSelected>
          {renderContextMenu && renderContextMenu()}
        </CardFooter>
      </StyledDashboardCard>
    </link_1.default>);
}
const AvatarWrapper = (0, styled_1.default)('span') `
  border: 3px solid ${p => p.theme.border};
  border-radius: 50%;
  height: min-content;
`;
const CardContent = (0, styled_1.default)('div') `
  flex-grow: 1;
  overflow: hidden;
  margin-right: ${(0, space_1.default)(1)};
`;
const StyledDashboardCard = (0, styled_1.default)(card_1.default) `
  justify-content: space-between;
  height: 100%;
  &:focus,
  &:hover {
    top: -1px;
  }
`;
const CardHeader = (0, styled_1.default)('div') `
  display: flex;
  padding: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(2)};
`;
const Title = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  ${overflowEllipsis_1.default};
`;
const Detail = (0, styled_1.default)('div') `
  font-family: ${p => p.theme.text.familyMono};
  font-size: ${p => p.theme.fontSizeSmall};
  color: ${p => p.theme.gray300};
  ${overflowEllipsis_1.default};
  line-height: 1.5;
`;
const CardBody = (0, styled_1.default)('div') `
  background: ${p => p.theme.gray100};
  padding: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(2)};
  max-height: 150px;
  min-height: 150px;
  overflow: hidden;
`;
const CardFooter = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
`;
const DateSelected = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  display: grid;
  grid-column-gap: ${(0, space_1.default)(1)};
  color: ${p => p.theme.textColor};
  ${overflowEllipsis_1.default};
`;
const DateStatus = (0, styled_1.default)('span') `
  color: ${p => p.theme.purple300};
  padding-left: ${(0, space_1.default)(1)};
`;
exports.default = DashboardCard;
//# sourceMappingURL=dashboardCard.jsx.map