Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const panelTable_1 = (0, tslib_1.__importDefault)(require("app/components/panels/panelTable"));
const userMisery_1 = (0, tslib_1.__importDefault)(require("app/components/userMisery"));
const platformCategories_1 = require("app/data/platformCategories");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const fields_1 = require("app/utils/discover/fields");
const constants_1 = require("app/utils/performance/vitals/constants");
const FRONTEND_PLATFORMS = [...platformCategories_1.frontend];
const BACKEND_PLATFORMS = [...platformCategories_1.backend, ...platformCategories_1.serverless];
const MOBILE_PLATFORMS = [...platformCategories_1.mobile];
class PerformanceCardTable extends React.PureComponent {
    userMiseryField() {
        return (<UserMiseryPanelItem>
        <StyledUserMisery bars={10} barHeight={20} miseryLimit={1000} totalUsers={500} userMisery={300} miserableUsers={200}/>
      </UserMiseryPanelItem>);
    }
    sectionField(field) {
        return (<StyledPanelItem>
        <TitleSpace />
        {field}
      </StyledPanelItem>);
    }
    renderFrontendPerformance() {
        const vitals = [fields_1.WebVital.FCP, fields_1.WebVital.FID, fields_1.WebVital.LCP, fields_1.WebVital.CLS];
        const webVitalTitles = vitals.map(vital => {
            return (<SubTitle key={vital}>
          {constants_1.WEB_VITAL_DETAILS[vital].name} ({constants_1.WEB_VITAL_DETAILS[vital].acronym})
        </SubTitle>);
        });
        const spans = ['HTTP', 'DB', 'Browser', 'Resource'];
        const spanTitles = spans.map(span => {
            return <SubTitle key={span}>{(0, locale_1.t)(span)}</SubTitle>;
        });
        // TODO(kelly): placeholder data. will need to add discover data for webvitals and span operations in follow-up pr
        const fieldData = ['0ms', '0ms', '0ms', '0ms'];
        const field = fieldData.map(data => {
            return (<Field key={data} align="right">
          {data}
        </Field>);
        });
        const columnData = () => {
            return (<div>
          {this.userMiseryField()}
          {this.sectionField(field)}
          {this.sectionField(field)}
        </div>);
        };
        return (<react_1.Fragment>
        <div>
          {/* Table description column */}
          <panels_1.PanelItem>{(0, locale_1.t)('User Misery')}</panels_1.PanelItem>
          <StyledPanelItem>
            <div>{(0, locale_1.t)('Web Vitals')}</div>
            {webVitalTitles}
          </StyledPanelItem>
          <StyledPanelItem>
            <div>{(0, locale_1.t)('Span Operations')}</div>
            {spanTitles}
          </StyledPanelItem>
        </div>
        <div>
          {/* Table All Releases column */}
          {/* TODO(kelly): placeholder data. will need to add user misery data in follow-up pr */}
          {columnData()}
        </div>
        <div>
          {/* Table This Release column */}
          {columnData()}
        </div>
        <div>
          {/* Table Change column */}
          {columnData()}
        </div>
      </react_1.Fragment>);
    }
    renderBackendPerformance() {
        const spans = ['HTTP', 'DB'];
        const spanTitles = spans.map(span => {
            return <SubTitle key={span}>{(0, locale_1.t)(span)}</SubTitle>;
        });
        // TODO(kelly): placeholder data. will need to add discover data for webvitals and span operations in follow-up pr
        const apdexData = ['0ms'];
        const apdexField = apdexData.map(data => {
            return (<Field key={data} align="right">
          {data}
        </Field>);
        });
        const fieldData = ['0ms', '0ms'];
        const field = fieldData.map(data => {
            return (<Field key={data} align="right">
          {data}
        </Field>);
        });
        const columnData = () => {
            return (<div>
          {this.userMiseryField()}
          <StyledPanelItem>{apdexField}</StyledPanelItem>
          {this.sectionField(field)}
        </div>);
        };
        return (<react_1.Fragment>
        <div>
          {/* Table description column */}
          <panels_1.PanelItem>{(0, locale_1.t)('User Misery')}</panels_1.PanelItem>
          <StyledPanelItem>
            <div>{(0, locale_1.t)('Apdex')}</div>
          </StyledPanelItem>
          <StyledPanelItem>
            <div>{(0, locale_1.t)('Span Operations')}</div>
            {spanTitles}
          </StyledPanelItem>
        </div>
        <div>
          {/* Table All Releases column */}
          {/* TODO(kelly): placeholder data. will need to add user misery data in follow-up pr */}
          {columnData()}
        </div>
        <div>
          {/* Table This Release column */}
          {columnData()}
        </div>
        <div>
          {/* Table Change column */}
          {columnData()}
        </div>
      </react_1.Fragment>);
    }
    renderMobilePerformance() {
        const mobileVitals = [
            fields_1.MobileVital.AppStartCold,
            fields_1.MobileVital.AppStartWarm,
            fields_1.MobileVital.FramesSlow,
            fields_1.MobileVital.FramesFrozenRate,
        ];
        const mobileVitalTitles = mobileVitals.map(mobileVital => {
            return (<panels_1.PanelItem key={mobileVital}>{constants_1.MOBILE_VITAL_DETAILS[mobileVital].name}</panels_1.PanelItem>);
        });
        // TODO(kelly): placeholder data. will need to add mobile data for mobilevitals in follow-up pr
        const mobileData = ['0ms'];
        const mobileField = mobileData.map(data => {
            return (<Field key={data} align="right">
          {data}
        </Field>);
        });
        const field = mobileVitals.map(vital => {
            return <StyledPanelItem key={vital}>{mobileField}</StyledPanelItem>;
        });
        const columnData = () => {
            return (<div>
          {this.userMiseryField()}
          {field}
        </div>);
        };
        return (<react_1.Fragment>
        <div>
          {/* Table description column */}
          <panels_1.PanelItem>{(0, locale_1.t)('User Misery')}</panels_1.PanelItem>
          {mobileVitalTitles}
        </div>
        <div>
          {/* Table All Releases column */}
          {/* TODO(kelly): placeholder data. will need to add user misery data in follow-up pr */}
          {columnData()}
        </div>
        <div>
          {/* Table This Release column */}
          {columnData()}
        </div>
        <div>
          {/* Table Change column */}
          {columnData()}
        </div>
      </react_1.Fragment>);
    }
    renderUnknownPerformance() {
        return (<react_1.Fragment>
        <div>
          {/* Table description column */}
          <panels_1.PanelItem>{(0, locale_1.t)('User Misery')}</panels_1.PanelItem>
        </div>
        <div>
          {/* TODO(kelly): placeholder data. will need to add user misery data in follow-up pr */}
          {this.userMiseryField()}
        </div>
        <div>
          {/* Table All Releases column */}
          {this.userMiseryField()}
        </div>
        <div>
          {/* Table This Release column */}
          {this.userMiseryField()}
        </div>
      </react_1.Fragment>);
    }
    render() {
        const { project, organization, isLoading, isEmpty } = this.props;
        // Custom set the height so we don't have layout shift when results are loaded.
        const loader = <loadingIndicator_1.default style={{ margin: '70px auto' }}/>;
        const title = FRONTEND_PLATFORMS.includes(project.platform)
            ? (0, locale_1.t)('Frontend Performance')
            : BACKEND_PLATFORMS.includes(project.platform)
                ? (0, locale_1.t)('Backend Performance')
                : MOBILE_PLATFORMS.includes(project.platform)
                    ? (0, locale_1.t)('Mobile Performance')
                    : (0, locale_1.t)('[Unknown] Performance');
        const platformPerformance = FRONTEND_PLATFORMS.includes(project.platform)
            ? this.renderFrontendPerformance()
            : BACKEND_PLATFORMS.includes(project.platform)
                ? this.renderBackendPerformance()
                : MOBILE_PLATFORMS.includes(project.platform)
                    ? this.renderMobilePerformance()
                    : this.renderUnknownPerformance();
        const isUnknownPlatform = ![
            ...FRONTEND_PLATFORMS,
            ...BACKEND_PLATFORMS,
            ...MOBILE_PLATFORMS,
        ].includes(project.platform);
        return (<react_1.Fragment>
        <HeadCellContainer>{title}</HeadCellContainer>
        {isUnknownPlatform ? (<StyledAlert type="warning" icon={<icons_1.IconWarning size="md"/>} system>
            For more performance metrics, specify which platform this project is using in{' '}
            <react_router_1.Link to={`/settings/${organization.slug}/projects/${project.slug}/`}>
              project settings.
            </react_router_1.Link>
          </StyledAlert>) : null}
        <StyledPanelTable isLoading={isLoading} isEmpty={isEmpty} emptyMessage={(0, locale_1.t)('No transactions found')} headers={[
                <Cell key="description" align="left">
              {(0, locale_1.t)('Description')}
            </Cell>,
                <Cell key="releases" align="right">
              {(0, locale_1.t)('All Releases')}
            </Cell>,
                <Cell key="release" align="right">
              {(0, locale_1.t)('This Release')}
            </Cell>,
                <Cell key="change" align="right">
              {(0, locale_1.t)('Change')}
            </Cell>,
            ]} disablePadding loader={loader} disableTopBorder={isUnknownPlatform}>
          {platformPerformance}
        </StyledPanelTable>
      </react_1.Fragment>);
    }
}
const HeadCellContainer = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeExtraLarge};
  padding: ${(0, space_1.default)(2)};
  border-top: 1px solid ${p => p.theme.border};
  border-left: 1px solid ${p => p.theme.border};
  border-right: 1px solid ${p => p.theme.border};
  border-top-left-radius: ${p => p.theme.borderRadius};
  border-top-right-radius: ${p => p.theme.borderRadius};
`;
const StyledPanelTable = (0, styled_1.default)(panelTable_1.default) `
  border-top-left-radius: 0;
  border-top-right-radius: 0;
  border-top: ${p => (p.disableTopBorder ? 'none' : `1px solid ${p.theme.border}`)};
  @media (max-width: ${p => p.theme.breakpoints[2]}) {
    grid-template-columns: min-content 1fr 1fr 1fr;
  }
`;
const StyledPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  display: block;
  white-space: nowrap;
  width: 100%;
`;
const SubTitle = (0, styled_1.default)('div') `
  margin-left: ${(0, space_1.default)(3)};
`;
const TitleSpace = (0, styled_1.default)('div') `
  height: 24px;
`;
const StyledUserMisery = (0, styled_1.default)(userMisery_1.default) `
  ${panels_1.PanelItem} {
    justify-content: flex-end;
  }
`;
const UserMiseryPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  justify-content: flex-end;
`;
const Field = (0, styled_1.default)('div') `
  text-align: ${p => p.align};
  margin-left: ${p => p.align === 'left' && (0, space_1.default)(2)};
`;
const Cell = (0, styled_1.default)('div') `
  text-align: ${p => p.align};
  margin-left: ${p => p.align === 'left' && (0, space_1.default)(2)};
  padding-right: ${p => p.align === 'right' && (0, space_1.default)(2)};
  ${overflowEllipsis_1.default}
`;
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  border-top: 1px solid ${p => p.theme.border};
  border-right: 1px solid ${p => p.theme.border};
  border-left: 1px solid ${p => p.theme.border};
  margin-bottom: 0;
`;
exports.default = PerformanceCardTable;
//# sourceMappingURL=performanceCardTable.jsx.map