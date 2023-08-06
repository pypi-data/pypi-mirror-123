Object.defineProperty(exports, "__esModule", { value: true });
exports.BorderlessEventEntries = void 0;
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const indicator_1 = require("app/actionCreators/indicator");
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const contexts_1 = (0, tslib_1.__importDefault)(require("app/components/events/contexts"));
const contextSummary_1 = (0, tslib_1.__importDefault)(require("app/components/events/contextSummary/contextSummary"));
const device_1 = (0, tslib_1.__importDefault)(require("app/components/events/device"));
const errors_1 = (0, tslib_1.__importDefault)(require("app/components/events/errors"));
const eventAttachments_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventAttachments"));
const eventCause_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventCause"));
const eventCauseEmpty_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventCauseEmpty"));
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const eventExtraData_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventExtraData/eventExtraData"));
const eventSdk_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventSdk"));
const eventTags_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventTags/eventTags"));
const groupingInfo_1 = (0, tslib_1.__importDefault)(require("app/components/events/groupingInfo"));
const packageData_1 = (0, tslib_1.__importDefault)(require("app/components/events/packageData"));
const rrwebIntegration_1 = (0, tslib_1.__importDefault)(require("app/components/events/rrwebIntegration"));
const sdkUpdates_1 = (0, tslib_1.__importDefault)(require("app/components/events/sdkUpdates"));
const styles_1 = require("app/components/events/styles");
const userFeedback_1 = (0, tslib_1.__importDefault)(require("app/components/events/userFeedback"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const event_1 = require("app/types/event");
const utils_1 = require("app/types/utils");
const utils_2 = require("app/utils");
const analytics_1 = require("app/utils/analytics");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const projectProcessingIssues_1 = require("app/views/settings/project/projectProcessingIssues");
const findBestThread_1 = (0, tslib_1.__importDefault)(require("./interfaces/threads/threadSelector/findBestThread"));
const getThreadException_1 = (0, tslib_1.__importDefault)(require("./interfaces/threads/threadSelector/getThreadException"));
const eventEntry_1 = (0, tslib_1.__importDefault)(require("./eventEntry"));
const eventTagsAndScreenshot_1 = (0, tslib_1.__importDefault)(require("./eventTagsAndScreenshot"));
const MINIFIED_DATA_JAVA_EVENT_REGEX_MATCH = /^(([\w\$]\.[\w\$]{1,2})|([\w\$]{2}\.[\w\$]\.[\w\$]))(\.|$)/g;
const EventEntries = (0, react_1.memo)(({ organization, project, location, api, event, group, className, router, route, isShare = false, showExampleCommit = false, showTagSummary = true, isBorderless = false, }) => {
    var _a, _b;
    const [isLoading, setIsLoading] = (0, react_1.useState)(true);
    const [proGuardErrors, setProGuardErrors] = (0, react_1.useState)([]);
    const [attachments, setAttachments] = (0, react_1.useState)([]);
    const orgSlug = organization.slug;
    const projectSlug = project.slug;
    const orgFeatures = (_a = organization === null || organization === void 0 ? void 0 : organization.features) !== null && _a !== void 0 ? _a : [];
    const hasEventAttachmentsFeature = orgFeatures.includes('event-attachments');
    (0, react_1.useEffect)(() => {
        checkProGuardError();
        recordIssueError();
        fetchAttachments();
    }, []);
    function recordIssueError() {
        if (!event || !event.errors || !(event.errors.length > 0)) {
            return;
        }
        const errors = event.errors;
        const errorTypes = errors.map(errorEntries => errorEntries.type);
        const errorMessages = errors.map(errorEntries => errorEntries.message);
        const orgId = organization.id;
        const platform = project.platform;
        (0, analytics_1.analytics)('issue_error_banner.viewed', Object.assign({ org_id: orgId ? parseInt(orgId, 10) : null, group: event === null || event === void 0 ? void 0 : event.groupID, error_type: errorTypes, error_message: errorMessages }, (platform && { platform })));
    }
    function fetchProguardMappingFiles(query) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            try {
                const proguardMappingFiles = yield api.requestPromise(`/projects/${orgSlug}/${projectSlug}/files/dsyms/`, {
                    method: 'GET',
                    query: {
                        query,
                        file_formats: 'proguard',
                    },
                });
                return proguardMappingFiles;
            }
            catch (error) {
                Sentry.captureException(error);
                // do nothing, the UI will not display extra error details
                return [];
            }
        });
    }
    function isDataMinified(str) {
        if (!str) {
            return false;
        }
        return !![...str.matchAll(MINIFIED_DATA_JAVA_EVENT_REGEX_MATCH)].length;
    }
    function hasThreadOrExceptionMinifiedFrameData(definedEvent, bestThread) {
        var _a, _b, _c, _d, _e, _f, _g;
        if (!bestThread) {
            const exceptionValues = (_d = (_c = (_b = (_a = definedEvent.entries) === null || _a === void 0 ? void 0 : _a.find(e => e.type === event_1.EntryType.EXCEPTION)) === null || _b === void 0 ? void 0 : _b.data) === null || _c === void 0 ? void 0 : _c.values) !== null && _d !== void 0 ? _d : [];
            return !!exceptionValues.find(exceptionValue => { var _a, _b; return (_b = (_a = exceptionValue.stacktrace) === null || _a === void 0 ? void 0 : _a.frames) === null || _b === void 0 ? void 0 : _b.find(frame => isDataMinified(frame.module)); });
        }
        const threadExceptionValues = (_e = (0, getThreadException_1.default)(definedEvent, bestThread)) === null || _e === void 0 ? void 0 : _e.values;
        return !!(threadExceptionValues
            ? threadExceptionValues.find(threadExceptionValue => {
                var _a, _b;
                return (_b = (_a = threadExceptionValue.stacktrace) === null || _a === void 0 ? void 0 : _a.frames) === null || _b === void 0 ? void 0 : _b.find(frame => isDataMinified(frame.module));
            })
            : (_g = (_f = bestThread === null || bestThread === void 0 ? void 0 : bestThread.stacktrace) === null || _f === void 0 ? void 0 : _f.frames) === null || _g === void 0 ? void 0 : _g.find(frame => isDataMinified(frame.module)));
    }
    function checkProGuardError() {
        var _a, _b, _c, _d, _e, _f, _g;
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (!event || event.platform !== 'java') {
                setIsLoading(false);
                return;
            }
            const hasEventErrorsProGuardMissingMapping = (_a = event.errors) === null || _a === void 0 ? void 0 : _a.find(error => error.type === 'proguard_missing_mapping');
            if (hasEventErrorsProGuardMissingMapping) {
                setIsLoading(false);
                return;
            }
            const newProGuardErrors = [];
            const debugImages = (_c = (_b = event.entries) === null || _b === void 0 ? void 0 : _b.find(e => e.type === event_1.EntryType.DEBUGMETA)) === null || _c === void 0 ? void 0 : _c.data.images;
            // When debugImages contains a 'proguard' entry, it must always be only one entry
            const proGuardImage = debugImages === null || debugImages === void 0 ? void 0 : debugImages.find(debugImage => (debugImage === null || debugImage === void 0 ? void 0 : debugImage.type) === 'proguard');
            const proGuardImageUuid = proGuardImage === null || proGuardImage === void 0 ? void 0 : proGuardImage.uuid;
            // If an entry is of type 'proguard' and has 'uuid',
            // it means that the Sentry Gradle plugin has been executed,
            // otherwise the proguard id wouldn't be in the event.
            // But maybe it failed to upload the mappings file
            if ((0, utils_2.defined)(proGuardImageUuid)) {
                if (isShare) {
                    setIsLoading(false);
                    return;
                }
                const proguardMappingFiles = yield fetchProguardMappingFiles(proGuardImageUuid);
                if (!proguardMappingFiles.length) {
                    newProGuardErrors.push({
                        type: 'proguard_missing_mapping',
                        message: projectProcessingIssues_1.projectProcessingIssuesMessages.proguard_missing_mapping,
                        data: { mapping_uuid: proGuardImageUuid },
                    });
                }
                setProGuardErrors(newProGuardErrors);
                setIsLoading(false);
                return;
            }
            else {
                if (proGuardImage) {
                    Sentry.withScope(function (s) {
                        s.setLevel(Sentry.Severity.Warning);
                        if (event.sdk) {
                            s.setTag('offending.event.sdk.name', event.sdk.name);
                            s.setTag('offending.event.sdk.version', event.sdk.version);
                        }
                        Sentry.captureMessage('Event contains proguard image but not uuid');
                    });
                }
            }
            const threads = (_g = (_f = (_e = (_d = event.entries) === null || _d === void 0 ? void 0 : _d.find(e => e.type === event_1.EntryType.THREADS)) === null || _e === void 0 ? void 0 : _e.data) === null || _f === void 0 ? void 0 : _f.values) !== null && _g !== void 0 ? _g : [];
            const bestThread = (0, findBestThread_1.default)(threads);
            const hasThreadOrExceptionMinifiedData = hasThreadOrExceptionMinifiedFrameData(event, bestThread);
            if (hasThreadOrExceptionMinifiedData) {
                newProGuardErrors.push({
                    type: 'proguard_potentially_misconfigured_plugin',
                    message: (0, locale_1.tct)('Some frames appear to be minified. Did you configure the [plugin]?', {
                        plugin: (<externalLink_1.default href="https://docs.sentry.io/platforms/android/proguard/#gradle">
                  Sentry Gradle Plugin
                </externalLink_1.default>),
                    }),
                });
                // This capture will be removed once we're confident with the level of effectiveness
                Sentry.withScope(function (s) {
                    s.setLevel(Sentry.Severity.Warning);
                    if (event.sdk) {
                        s.setTag('offending.event.sdk.name', event.sdk.name);
                        s.setTag('offending.event.sdk.version', event.sdk.version);
                    }
                    Sentry.captureMessage(!proGuardImage
                        ? 'No Proguard is used at all, but a frame did match the regex'
                        : "Displaying ProGuard warning 'proguard_potentially_misconfigured_plugin' for suspected event");
                });
            }
            setProGuardErrors(newProGuardErrors);
            setIsLoading(false);
        });
    }
    function fetchAttachments() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (!event || isShare || !hasEventAttachmentsFeature) {
                return;
            }
            try {
                const response = yield api.requestPromise(`/projects/${orgSlug}/${projectSlug}/events/${event.id}/attachments/`);
                setAttachments(response);
            }
            catch (error) {
                Sentry.captureException(error);
                (0, indicator_1.addErrorMessage)('An error occurred while fetching attachments');
            }
        });
    }
    function renderEntries(definedEvent) {
        const entries = definedEvent.entries;
        if (!Array.isArray(entries)) {
            return null;
        }
        return entries.map((entry, entryIdx) => (<errorBoundary_1.default key={`entry-${entryIdx}`} customComponent={<eventDataSection_1.default type={entry.type} title={entry.type}>
              <p>{(0, locale_1.t)('There was an error rendering this data.')}</p>
            </eventDataSection_1.default>}>
          <eventEntry_1.default projectSlug={projectSlug} group={group} organization={organization} event={definedEvent} entry={entry} route={route} router={router}/>
        </errorBoundary_1.default>));
    }
    function handleDeleteAttachment(attachmentId) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (!event) {
                return;
            }
            try {
                yield api.requestPromise(`/projects/${orgSlug}/${projectSlug}/events/${event.id}/attachments/${attachmentId}/`, {
                    method: 'DELETE',
                });
                setAttachments(attachments.filter(attachment => attachment.id !== attachmentId));
            }
            catch (error) {
                Sentry.captureException(error);
                (0, indicator_1.addErrorMessage)('An error occurred while deleteting the attachment');
            }
        });
    }
    if (!event) {
        return (<LatestEventNotAvailable>
          <h3>{(0, locale_1.t)('Latest Event Not Available')}</h3>
        </LatestEventNotAvailable>);
    }
    const hasMobileScreenshotsFeature = orgFeatures.includes('mobile-screenshots');
    const hasContext = !(0, utils_2.objectIsEmpty)(event.user) || !(0, utils_2.objectIsEmpty)(event.contexts);
    const hasErrors = !(0, utils_2.objectIsEmpty)(event.errors) || !!proGuardErrors.length;
    return (<div className={className} data-test-id={`event-entries-loading-${isLoading}`}>
        {hasErrors && !isLoading && (<errors_1.default event={event} orgSlug={orgSlug} projectSlug={projectSlug} proGuardErrors={proGuardErrors}/>)}
        {!isShare &&
            (0, utils_1.isNotSharedOrganization)(organization) &&
            (showExampleCommit ? (<eventCauseEmpty_1.default event={event} organization={organization} project={project}/>) : (<eventCause_1.default organization={organization} project={project} event={event} group={group}/>))}
        {event.userReport && group && (<StyledEventUserFeedback report={event.userReport} orgId={orgSlug} issueId={group.id} includeBorder={!hasErrors}/>)}
        {showTagSummary &&
            (hasMobileScreenshotsFeature ? (<eventTagsAndScreenshot_1.default event={event} organization={organization} projectId={projectSlug} location={location} isShare={isShare} hasContext={hasContext} isBorderless={isBorderless} attachments={attachments} onDeleteScreenshot={handleDeleteAttachment}/>) : ((!!((_b = event.tags) !== null && _b !== void 0 ? _b : []).length || hasContext) && (<StyledEventDataSection title={(0, locale_1.t)('Tags')} type="tags">
                {hasContext && <contextSummary_1.default event={event}/>}
                <eventTags_1.default event={event} organization={organization} projectId={projectSlug} location={location}/>
              </StyledEventDataSection>)))}
        {renderEntries(event)}
        {hasContext && <contexts_1.default group={group} event={event}/>}
        {event && !(0, utils_2.objectIsEmpty)(event.context) && <eventExtraData_1.default event={event}/>}
        {event && !(0, utils_2.objectIsEmpty)(event.packages) && <packageData_1.default event={event}/>}
        {event && !(0, utils_2.objectIsEmpty)(event.device) && <device_1.default event={event}/>}
        {!isShare && hasEventAttachmentsFeature && (<eventAttachments_1.default event={event} orgId={orgSlug} projectId={projectSlug} location={location} attachments={attachments} onDeleteAttachment={handleDeleteAttachment}/>)}
        {event.sdk && !(0, utils_2.objectIsEmpty)(event.sdk) && <eventSdk_1.default sdk={event.sdk}/>}
        {!isShare && (event === null || event === void 0 ? void 0 : event.sdkUpdates) && event.sdkUpdates.length > 0 && (<sdkUpdates_1.default event={Object.assign({ sdkUpdates: event.sdkUpdates }, event)}/>)}
        {!isShare && event.groupID && (<groupingInfo_1.default projectId={projectSlug} event={event} showGroupingConfig={orgFeatures.includes('set-grouping-config')}/>)}
        {!isShare && hasEventAttachmentsFeature && (<rrwebIntegration_1.default event={event} orgId={orgSlug} projectId={projectSlug}/>)}
      </div>);
});
const LatestEventNotAvailable = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(4)};
`;
const ErrorContainer = (0, styled_1.default)('div') `
  /*
  Remove border on adjacent context summary box.
  Once that component uses emotion this will be harder.
  */
  & + .context-summary {
    border-top: none;
  }
`;
const BorderlessEventEntries = (0, styled_1.default)(EventEntries) `
  & ${ /* sc-selector */styles_1.DataSection} {
    padding: ${(0, space_1.default)(3)} 0 0 0;
  }
  & ${ /* sc-selector */styles_1.DataSection}:first-child {
    padding-top: 0;
    border-top: 0;
  }
  & ${ /* sc-selector */ErrorContainer} {
    margin-bottom: ${(0, space_1.default)(2)};
  }
`;
exports.BorderlessEventEntries = BorderlessEventEntries;
const StyledEventUserFeedback = (0, styled_1.default)(userFeedback_1.default) `
  border-radius: 0;
  box-shadow: none;
  padding: ${(0, space_1.default)(3)} ${(0, space_1.default)(4)} 0 40px;
  border: 0;
  ${p => (p.includeBorder ? `border-top: 1px solid ${p.theme.innerBorder};` : '')}
  margin: 0;
`;
const StyledEventDataSection = (0, styled_1.default)(eventDataSection_1.default) `
  margin-bottom: ${(0, space_1.default)(2)};
`;
// TODO(ts): any required due to our use of SharedViewOrganization
exports.default = (0, withOrganization_1.default)((0, withApi_1.default)(EventEntries));
//# sourceMappingURL=eventEntries.jsx.map