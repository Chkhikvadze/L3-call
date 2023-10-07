import Textarea from '@l3-lib/ui-core/dist/Textarea'
import Typography from '@l3-lib/ui-core/dist/Typography'

import FormikTextField from 'components/TextFieldFormik'
import {
  StyledForm,
  StyledInputWrapper,
  StyledRoot,
  StyledTextareaWrapper,
} from 'pages/Agents/AgentForm/AgentForm'
import TypographyPrimary from 'components/Typography/Primary'
import { useScheduleForm } from './useScheduleForm'
import AgentDropdown from 'pages/Agents/AgentForm/components/AgentDropdown'

const ScheduleForm = ({ formik }: { formik: any }) => {
  const { values, setFieldValue } = formik
  const { schedule_description, schedule_group_id, schedule_agent_id } = values

  const onDescriptionChange = (value: string) => {
    setFieldValue('schedule_description', value)
  }

  const { agentOptions, groupOptions } = useScheduleForm()

  return (
    <StyledRoot>
      <StyledForm>
        <StyledInputWrapper>
          <FormikTextField name='schedule_name' placeholder='Name' label='Name' />

          <FormikTextField name='schedule_type' placeholder='Type' label='Type' />

          <FormikTextField
            name='schedule_cron_expression'
            placeholder='Cron expression'
            label='Cron expression'
          />

          <StyledTextareaWrapper>
            <TypographyPrimary
              value='Description'
              type={Typography.types.LABEL}
              size={Typography.sizes.md}
            />
            <Textarea
              hint=''
              placeholder='Description'
              name='schedule_description'
              value={schedule_description}
              onChange={onDescriptionChange}
            />
          </StyledTextareaWrapper>

          <AgentDropdown
            label={'Agent'}
            fieldName={'schedule_agent_id'}
            setFieldValue={setFieldValue}
            fieldValue={schedule_agent_id}
            options={agentOptions}
            optionSize={'small'}
          />
          <AgentDropdown
            label={'Group'}
            fieldName={'schedule_group_id'}
            setFieldValue={setFieldValue}
            fieldValue={schedule_group_id}
            options={groupOptions}
            optionSize={'small'}
          />
        </StyledInputWrapper>
      </StyledForm>
    </StyledRoot>
  )
}

export default ScheduleForm
