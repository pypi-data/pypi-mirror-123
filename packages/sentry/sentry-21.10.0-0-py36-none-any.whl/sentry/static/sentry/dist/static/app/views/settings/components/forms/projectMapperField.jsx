Object.defineProperty(exports, "__esModule", { value: true });
exports.RenderField = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_select_1 = require("react-select");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const removeAtArrayIndex_1 = require("app/utils/removeAtArrayIndex");
const fieldErrorReason_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldErrorReason"));
const controlState_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formField/controlState"));
const inputField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/inputField"));
// Get the icon
const getIcon = (iconType) => {
    switch (iconType) {
        case 'vercel':
            return <icons_1.IconVercel />;
        default:
            return <icons_1.IconGeneric />;
    }
};
class RenderField extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = { selectedSentryProjectId: null, selectedMappedValue: null };
    }
    render() {
        const { onChange, onBlur, value: incomingValues, sentryProjects, mappedDropdown: { items: mappedDropdownItems, placeholder: mappedValuePlaceholder }, nextButton: { text: nextButtonText, description: nextDescription, allowedDomain }, iconType, model, id: formElementId, error, } = this.props;
        const existingValues = incomingValues || [];
        const nextUrlOrArray = (0, integrationUtil_1.safeGetQsParam)('next');
        let nextUrl = Array.isArray(nextUrlOrArray) ? nextUrlOrArray[0] : nextUrlOrArray;
        if (nextUrl && !nextUrl.startsWith(allowedDomain)) {
            // eslint-disable-next-line no-console
            console.warn(`Got unexpected next url: ${nextUrl}`);
            nextUrl = undefined;
        }
        const { selectedSentryProjectId, selectedMappedValue } = this.state;
        // create maps by the project id for constant time lookups
        const sentryProjectsById = Object.fromEntries(sentryProjects.map(project => [project.id, project]));
        const mappedItemsByValue = Object.fromEntries(mappedDropdownItems.map(item => [item.value, item]));
        // build sets of values used so we don't let the user select them twice
        const projectIdsUsed = new Set(existingValues.map(tuple => tuple[0]));
        const mappedValuesUsed = new Set(existingValues.map(tuple => tuple[1]));
        const projectOptions = sentryProjects
            .filter(project => !projectIdsUsed.has(project.id))
            .map(({ slug, id }) => ({ label: slug, value: id }));
        const mappedItemsToShow = mappedDropdownItems.filter(item => !mappedValuesUsed.has(item.value));
        const handleSelectProject = ({ value }) => {
            this.setState({ selectedSentryProjectId: value });
        };
        const handleSelectMappedValue = ({ value }) => {
            this.setState({ selectedMappedValue: value });
        };
        const handleAdd = () => {
            // add the new value to the list of existing values
            const projectMappings = [
                ...existingValues,
                [selectedSentryProjectId, selectedMappedValue],
            ];
            // trigger events so we save the value and show the check mark
            onChange === null || onChange === void 0 ? void 0 : onChange(projectMappings, []);
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(projectMappings, []);
            this.setState({ selectedSentryProjectId: null, selectedMappedValue: null });
        };
        const handleDelete = (index) => {
            const projectMappings = (0, removeAtArrayIndex_1.removeAtArrayIndex)(existingValues, index);
            // trigger events so we save the value and show the check mark
            onChange === null || onChange === void 0 ? void 0 : onChange(projectMappings, []);
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(projectMappings, []);
        };
        const renderItem = (itemTuple, index) => {
            const [projectId, mappedValue] = itemTuple;
            const project = sentryProjectsById[projectId];
            // TODO: add special formatting if deleted
            const mappedItem = mappedItemsByValue[mappedValue];
            return (<Item key={index}>
          <MappedProjectWrapper>
            {project ? (<idBadge_1.default project={project} avatarSize={20} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>) : ((0, locale_1.t)('Deleted'))}
            <icons_1.IconArrow size="xs" direction="right"/>
          </MappedProjectWrapper>
          <MappedItemValue>
            {mappedItem ? (<react_1.Fragment>
                <IntegrationIconWrapper>{getIcon(iconType)}</IntegrationIconWrapper>
                {mappedItem.label}
                <StyledExternalLink href={mappedItem.url}>
                  <icons_1.IconOpen size="xs"/>
                </StyledExternalLink>
              </react_1.Fragment>) : ((0, locale_1.t)('Deleted'))}
          </MappedItemValue>
          <DeleteButtonWrapper>
            <button_1.default onClick={() => handleDelete(index)} icon={<icons_1.IconDelete color="gray300"/>} size="small" type="button" aria-label={(0, locale_1.t)('Delete')}/>
          </DeleteButtonWrapper>
        </Item>);
        };
        const customValueContainer = containerProps => {
            // if no value set, we want to return the default component that is rendered
            const project = sentryProjectsById[selectedSentryProjectId || ''];
            if (!project) {
                return <react_select_1.components.ValueContainer {...containerProps}/>;
            }
            return (<react_select_1.components.ValueContainer {...containerProps}>
          <idBadge_1.default project={project} avatarSize={20} displayName={project.slug} avatarProps={{ consistentWidth: true }} disableLink/>
        </react_select_1.components.ValueContainer>);
        };
        const customOptionProject = projectProps => {
            const project = sentryProjectsById[projectProps.value];
            // Should never happen for a dropdown item
            if (!project) {
                return null;
            }
            return (<react_select_1.components.Option {...projectProps}>
          <idBadge_1.default project={project} avatarSize={20} displayName={project.slug} avatarProps={{ consistentWidth: true }} disableLink/>
        </react_select_1.components.Option>);
        };
        const customMappedValueContainer = containerProps => {
            // if no value set, we want to return the default component that is rendered
            const mappedValue = mappedItemsByValue[selectedMappedValue || ''];
            if (!mappedValue) {
                return <react_select_1.components.ValueContainer {...containerProps}/>;
            }
            return (<react_select_1.components.ValueContainer {...containerProps}>
          <IntegrationIconWrapper>{getIcon(iconType)}</IntegrationIconWrapper>
          <OptionLabelWrapper>{mappedValue.label}</OptionLabelWrapper>
        </react_select_1.components.ValueContainer>);
        };
        const customOptionMappedValue = optionProps => {
            return (<react_select_1.components.Option {...optionProps}>
          <OptionWrapper>
            <IntegrationIconWrapper>{getIcon(iconType)}</IntegrationIconWrapper>
            <OptionLabelWrapper>{optionProps.label}</OptionLabelWrapper>
          </OptionWrapper>
        </react_select_1.components.Option>);
        };
        return (<react_1.Fragment>
        {existingValues.map(renderItem)}
        <Item>
          <selectControl_1.default placeholder={(0, locale_1.t)('Sentry project\u2026')} name="project" options={projectOptions} components={{
                Option: customOptionProject,
                ValueContainer: customValueContainer,
            }} onChange={handleSelectProject} value={selectedSentryProjectId}/>
          <selectControl_1.default placeholder={mappedValuePlaceholder} name="mappedDropdown" options={mappedItemsToShow} components={{
                Option: customOptionMappedValue,
                ValueContainer: customMappedValueContainer,
            }} onChange={handleSelectMappedValue} value={selectedMappedValue}/>
          <AddProjectWrapper>
            <button_1.default type="button" disabled={!selectedSentryProjectId || !selectedMappedValue} size="small" priority="primary" onClick={handleAdd} icon={<icons_1.IconAdd />}/>
          </AddProjectWrapper>
          <FieldControlWrapper>
            {formElementId && (<div>
                <controlState_1.default model={model} name={formElementId}/>
                {error ? <StyledFieldErrorReason>{error}</StyledFieldErrorReason> : null}
              </div>)}
          </FieldControlWrapper>
        </Item>
        {nextUrl && (<NextButtonPanelAlert icon={false} type="muted">
            <NextButtonWrapper>
              {nextDescription !== null && nextDescription !== void 0 ? nextDescription : ''}
              <button_1.default type="button" size="small" priority="primary" icon={<icons_1.IconOpen size="xs" color="white"/>} href={nextUrl}>
                {nextButtonText}
              </button_1.default>
            </NextButtonWrapper>
          </NextButtonPanelAlert>)}
      </react_1.Fragment>);
    }
}
exports.RenderField = RenderField;
const ProjectMapperField = (props) => (<StyledInputField {...props} resetOnError inline={false} stacked={false} hideControlState field={(renderProps) => <RenderField {...renderProps}/>}/>);
exports.default = ProjectMapperField;
const MappedProjectWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-right: ${(0, space_1.default)(1)};
`;
const Item = (0, styled_1.default)('div') `
  min-height: 60px;
  padding: ${(0, space_1.default)(2)};

  &:not(:last-child) {
    border-bottom: 1px solid ${p => p.theme.innerBorder};
  }

  display: grid;
  grid-column-gap: ${(0, space_1.default)(1)};
  align-items: center;
  grid-template-columns: 2.5fr 2.5fr max-content 30px;
  grid-template-areas: 'sentry-project mapped-value manage-project field-control';
`;
const MappedItemValue = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: max-content;
  align-items: center;
  grid-gap: ${(0, space_1.default)(1)};
  width: 100%;
`;
const DeleteButtonWrapper = (0, styled_1.default)('div') `
  grid-area: manage-project;
`;
const IntegrationIconWrapper = (0, styled_1.default)('span') `
  display: flex;
  align-items: center;
`;
const AddProjectWrapper = (0, styled_1.default)('div') `
  grid-area: manage-project;
`;
const OptionLabelWrapper = (0, styled_1.default)('div') `
  margin-left: ${(0, space_1.default)(0.5)};
`;
const StyledInputField = (0, styled_1.default)(inputField_1.default) `
  padding: 0;
`;
const StyledExternalLink = (0, styled_1.default)(externalLink_1.default) `
  display: flex;
`;
const OptionWrapper = (0, styled_1.default)('div') `
  align-items: center;
  display: flex;
`;
const FieldControlWrapper = (0, styled_1.default)('div') `
  position: relative;
  grid-area: field-control;
`;
const NextButtonPanelAlert = (0, styled_1.default)(panels_1.PanelAlert) `
  align-items: center;
  margin-bottom: -1px;
  border-bottom-left-radius: ${p => p.theme.borderRadius};
  border-bottom-right-radius: ${p => p.theme.borderRadius};
`;
const NextButtonWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr max-content;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
`;
const StyledFieldErrorReason = (0, styled_1.default)(fieldErrorReason_1.default) ``;
//# sourceMappingURL=projectMapperField.jsx.map