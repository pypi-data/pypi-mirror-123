Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importStar)(require("react"));
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const breadcrumbs_1 = require("app/types/breadcrumbs");
const category_1 = (0, tslib_1.__importDefault)(require("./category"));
const data_1 = (0, tslib_1.__importDefault)(require("./data"));
const level_1 = (0, tslib_1.__importDefault)(require("./level"));
const time_1 = (0, tslib_1.__importDefault)(require("./time"));
const type_1 = (0, tslib_1.__importDefault)(require("./type"));
const Breadcrumb = (0, react_1.memo)(function Breadcrumb({ organization, event, breadcrumb, relativeTime, displayRelativeTime, searchTerm, onLoad, scrollbarSize, style, route, router, ['data-test-id']: dataTestId, }) {
    const { type, description, color, level, category, timestamp } = breadcrumb;
    const error = breadcrumb.type === breadcrumbs_1.BreadcrumbType.ERROR;
    return (<Wrapper style={style} error={error} onLoad={onLoad} data-test-id={dataTestId} scrollbarSize={scrollbarSize}>
      <type_1.default type={type} color={color} description={description} error={error}/>
      <category_1.default category={category} searchTerm={searchTerm}/>
      <data_1.default event={event} organization={organization} breadcrumb={breadcrumb} searchTerm={searchTerm} route={route} router={router}/>
      <div>
        <level_1.default level={level} searchTerm={searchTerm}/>
      </div>
      <time_1.default timestamp={timestamp} relativeTime={relativeTime} displayRelativeTime={displayRelativeTime} searchTerm={searchTerm}/>
    </Wrapper>);
});
exports.default = Breadcrumb;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 64px 140px 1fr 106px 100px ${p => p.scrollbarSize}px;

  > * {
    padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  }

  @media (max-width: ${props => props.theme.breakpoints[0]}) {
    grid-template-rows: repeat(2, auto);
    grid-template-columns: max-content 1fr 74px 82px ${p => p.scrollbarSize}px;

    > * {
      padding: ${(0, space_1.default)(1)};

      /* Type */
      :nth-child(5n-4) {
        grid-row: 1/-1;
        padding-right: 0;
        padding-left: 0;
        margin-left: ${(0, space_1.default)(2)};
        margin-right: ${(0, space_1.default)(1)};
      }

      /* Data */
      :nth-child(5n-2) {
        grid-row: 2/2;
        grid-column: 2/-1;
        padding-top: 0;
        padding-right: ${(0, space_1.default)(2)};
      }

      /* Level */
      :nth-child(5n-1) {
        padding-right: 0;
        display: flex;
        justify-content: flex-end;
        align-items: flex-start;
      }

      /* Time */
      :nth-child(5n) {
        padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
      }
    }
  }

  word-break: break-all;
  white-space: pre-wrap;
  :not(:last-child) {
    border-bottom: 1px solid ${p => (p.error ? p.theme.red300 : p.theme.innerBorder)};
  }

  ${p => p.error &&
    (0, react_2.css) `
      :after {
        content: '';
        position: absolute;
        top: -1px;
        left: 0;
        height: 1px;
        width: 100%;
        background: ${p.theme.red300};
      }
    `}
`;
//# sourceMappingURL=index.jsx.map