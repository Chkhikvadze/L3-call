import { useCreateScheduleService } from 'services/schedule/useCreateScheduleService'
import { useSchedulesService } from 'services/schedule/useSchedulesService'

import { ButtonPrimary } from 'components/Button/Button'
import ComponentsWrapper from 'components/ComponentsWrapper/ComponentsWrapper'

import { StyledCardsWrapper } from 'pages/Agents/Agents'

import {
  StyledHeaderGroup,
  StyledSectionTitle,
  StyledSectionWrapper,
} from 'pages/Home/homeStyle.css'

import { useNavigate } from 'react-router-dom'
import TempCard from 'pages/Group/TempCard'

const Schedules = () => {
  const navigate = useNavigate()

  const { data: schedules } = useSchedulesService()
  const [createScheduleService] = useCreateScheduleService()

  return (
    <StyledSectionWrapper>
      <StyledHeaderGroup className='header_group'>
        <div>
          <StyledSectionTitle>Schedules</StyledSectionTitle>
          {/* <StyledSectionDescription>
        Here is your datasource, a collection of databases, APIs, files, and more.
      </StyledSectionDescription> */}
        </div>
        <div>
          <ButtonPrimary onClick={() => navigate('/schedules/create-schedule')} size={'small'}>
            Add Schedule
          </ButtonPrimary>
        </div>
      </StyledHeaderGroup>

      <ComponentsWrapper noPadding>
        <StyledCardsWrapper>
          {schedules?.map((group: any) => {
            return (
              <TempCard
                key={group.id}
                name={group.name}
                description={group.description}
                // onDeleteClick={() => deleteGroupHandler(group.id)}
              />
            )
          })}
        </StyledCardsWrapper>
      </ComponentsWrapper>
    </StyledSectionWrapper>
  )
}

export default Schedules
