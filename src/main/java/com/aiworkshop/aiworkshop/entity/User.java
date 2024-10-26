package com.aiworkshop.aiworkshop.entity;

import java.util.Collection;
import java.util.List;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "users")
@Schema(description = "Пользователь")
public class User implements UserDetails {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Schema(description = "ID пользователя", example = "1")
    private Long id;

    @Column(name = "username", unique = true)
    @Schema(description = "Имя пользователя", example = "login")
    private String username;

    @Column(name = "email")
    @Schema(description = "Email пользователя", example = "email@email.ru")
    private String email;

    @Column(name = "password")
    @Schema(description = "Пароль пользователя", example = "password")
    private String password;

    @OneToMany(mappedBy = "user")
    @Schema(description = "Статьи пользователя")
    private List<Article> articles;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "role_id")
    @Schema(description = "Роль пользователя")
    private Role role;

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return List.of();
    }

}
