import { ButtonPrimary } from 'components/Button/Button'
import ComponentsWrapper from 'components/ComponentsWrapper/ComponentsWrapper'

import { StyledCardsWrapper } from 'pages/Agents/Agents'

import {
  StyledHeaderGroup,
  StyledSectionTitle,
  StyledSectionWrapper,
} from 'pages/Home/homeStyle.css'

import { useNavigate } from 'react-router-dom'

import TempCard from './TempCard'
import { useGroups } from './useGroups'

const Groups = () => {
  const { groups, deleteGroupHandler } = useGroups()

  const navigate = useNavigate()

  return (
    <StyledSectionWrapper>
      <StyledHeaderGroup className='header_group'>
        <div>
          <StyledSectionTitle>Groups</StyledSectionTitle>
          {/* <StyledSectionDescription>
            Here is your datasource, a collection of databases, APIs, files, and more.
          </StyledSectionDescription> */}
        </div>
        <div>
          <ButtonPrimary onClick={() => navigate('/groups/create-group')} size={'small'}>
            Add Group
          </ButtonPrimary>
        </div>
      </StyledHeaderGroup>

      <ComponentsWrapper noPadding>
        <StyledCardsWrapper>
          {groups?.map((group: any) => {
            return (
              <TempCard
                key={group.id}
                name={group.name}
                description={group.description}
                onDeleteClick={() => deleteGroupHandler(group.id)}
              />
            )
          })}
        </StyledCardsWrapper>
      </ComponentsWrapper>
    </StyledSectionWrapper>
  )
}

export default Groups
